"""Mock SMTP Server."""
from hitchsmtp import smtperrors
import asyncore
import optparse
import signal
import email
import smtpd
import json
import sys
import re


if sys.version_info[0] >= 3:
    from email.parser import Parser
else:
    from email.Parser import Parser


class MockSMTPServer(smtpd.SMTPServer):
    """Mock SMTP server."""
    def __init__(*args, **kwargs):
        smtpd.SMTPServer.__init__(*args, **kwargs)

    def process_message(self, host, email_from, email_to, data):
        """Parse SMTP message and log it to the console as JSON."""
        parsed_message = Parser().parsestr(data)
        links_regex = re.compile(r"(https?://\S+)")

        if parsed_message.is_multipart():
            payload = []
            links = []
            for message in parsed_message.get_payload():
                payload_dict = dict(message)
                payload_dict['filename'] = message.get_filename()
                payload_dict['content'] = message.get_payload(decode=True).decode("utf-8")
                payload_dict['links'] = re.findall(links_regex, message.get_payload(decode=True).decode("utf-8"))
                links = links + payload_dict['links']
                payload.append(payload_dict)
        else:
            payload = parsed_message.get_payload()
            links = re.findall(links_regex, payload)

        header_from = parsed_message.get('From')
        header_to = parsed_message.get('To')
        email_regex = re.compile(r"^(.*?)\<(.*?)\>$")

        if header_from:
            header_from_name = email_regex.match(header_from).group(1).strip() if email_regex.match(header_from) else None
            header_from_email = email_regex.match(header_from).group(2) if email_regex.match(header_from) else None
        else:
            header_from_name = header_from_email = None

        if header_to:
            header_to_name = email_regex.match(header_to).group(1).strip() if email_regex.match(header_to) else None
            header_to_email = email_regex.match(header_to).group(2) if email_regex.match(header_to) else None
        else:
            header_to_name = header_to_email = None


        dict_message = {
            'sent_from': email_from,
            'sent_to': email_to,
            'header_from': header_from,
            'header_to': header_to,
            'header_from_name': header_from_name,
            'header_to_name': header_to_name,
            'header_from_email': header_from_email,
            'header_to_email': header_to_email,
            'subject': parsed_message.get('Subject'),
            'date': parsed_message.get('Date'),
            'contenttype': parsed_message.get_content_type(),
            'multipart': parsed_message.is_multipart(),
            'payload': payload,
            'links': links,
        }
        sys.stdout.write(json.dumps(dict_message))
        sys.stdout.write('\n')
        sys.stdout.flush()

        if len(email_to) > 0:
            if email_to[0].endswith("@smtperrors.com"):
                name = email_to[0].replace("@smtperrors.com", "")
                if name in smtperrors.errors:
                    return smtperrors.errors[name]
                else:
                    raise Exception("{0} was not found in the list of SMTP errors.")


def server(port_number=10025):
    """Python library interface."""
    if port_number < 1024:
        sys.stderr.write("WARNING: Using a port below 1024 to run test Internet services"
                         " on is normally prohibited for non-root users, and usually inadvisable.\n\n")
        sys.stderr.flush()

    sys.stdout.write("SMTP Server running\n")
    sys.stdout.flush()

    smtp_server = MockSMTPServer(('localhost', port_number), None)

    def signal_handler(signal, frame):
        print('')
        smtp_server.close()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    asyncore.loop()


def main():
    """CLI interface."""
    parser = optparse.OptionParser()
    parser.add_option("-p", "--port", type="int", dest="smtp_port", default=10025,
                      help="Specify the port number for the mock SMTP server to run on (default: 10025).")

    options, _ = parser.parse_args(sys.argv[1:])
    server(port_number=options.smtp_port)


if __name__ == '__main__':
    main()
