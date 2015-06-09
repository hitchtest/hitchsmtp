from hitchserve import ServiceBundle, Interactive, HitchTraceback, Service
from os import path, system, chdir
from subprocess import call
import hitchenvironment
import unittest
import os

# Get directory above this file
PROJECT_DIRECTORY = path.abspath(path.join(path.dirname(__file__), '..'))

class HitchSMTPExecutionEngine(unittest.TestCase):
    """Engine for orchestating and interacting with the reminders app."""
    settings = {}
    preconditions = {}

    def setUp(self):
        """Ensure virtualenv present, then run all services."""
        chdir(PROJECT_DIRECTORY)
        venv_dir = os.path.join(PROJECT_DIRECTORY, "venv{}".format(
            self.preconditions['python_version'])
        )
        if not path.exists(venv_dir):
            call([
                    "virtualenv", "--no-site-packages", "--distribute",
                    "-p", "/usr/bin/python{}".format(self.preconditions['python_version']),
                    venv_dir,
                ])

        venv_python = os.path.join(venv_dir, "bin", "python")
        call([venv_python, "setup.py", "install", ])
        environment = hitchenvironment.Environment(
            self.settings["platform"],
            self.settings["systembits"],
            self.settings["requires_internet"],
        )

        self.services = ServiceBundle(
            project_directory=PROJECT_DIRECTORY,
            environment=environment,
            startup_timeout=float(self.settings["startup_timeout"]),
            shutdown_timeout=1.0,
        )

        self.services['HitchSMTP'] = Service(
            command=[venv_python, "-m", "hitchsmtp.smtp",],
            log_line_ready_checker=lambda line: line == "SMTP Server running",
        )

        self.services.startup(interactive=False)

    def send_mail(self, host="localhost", port="10025", from_address="", to_address="", body="", raises=None):
        """Send email using standard libs."""
        import smtplib
        server = smtplib.SMTP(host=host, port=int(port))
        server.set_debuglevel(bool(self.settings["smtp_debug_messages"]))
        if raises is None:
            server.sendmail(from_address, [to_address], body)
        else:
            exec("smtperror = {}".format(raises))
            self.assertRaises(smtperror, server.sendmail, from_address, [to_address], body)
        server.quit()

    def send_multipart_mail(self, port="10025", application="octet-stream", from_address="", to_address="", message=None):
        import smtplib
        from email import Encoders
        from email.MIMEBase import MIMEBase
        from email.MIMEMultipart import MIMEMultipart
        from email.Utils import formatdate

        server = smtplib.SMTP(host="localhost", port=int(port))
        server.set_debuglevel(bool(self.settings["smtp_debug_messages"]))

        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = to_address
        msg["Subject"] = message['Subject']
        msg['Date'] = formatdate(localtime=True)

        with open(message['Attachment'], "rb") as payload_h:
            payload = payload_h.read()

        # Attach the file
        part = MIMEBase('application', application)
        part.set_payload(payload)
        Encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            'attachment; filename="{0}"'.format(os.path.basename(message['Attachment']))
        )
        msg.attach(part)

        server.sendmail(from_address, [to_address], msg.as_string())
        server.quit()

    def check_for_attachment(self, filename):
        with open(filename, "rb") as payload_h:
            payload = payload_h.read()
        self.assertEquals(self.received_email['payload'][0]['content'], payload)

    def wait_for_email(self):
        self.received_email = self.services['HitchSMTP'].logs.out.tail.until_json(
            lambda email: True,
            timeout=1,
            lines_back=1,
        )

    def check_email_property(self, **kwargs):
        for key, value in kwargs.items():
            self.assertEquals(self.received_email[key], value)

    def tearDown(self):
        """We're done here."""
        if hasattr(self, 'services'):
            self.services.shutdown()