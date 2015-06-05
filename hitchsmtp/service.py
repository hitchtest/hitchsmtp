import subprocess
import hitchserve
import sys
import os

# TODO: Create email object to signify email, address and attachment.
# TODO: "Wait until email arrives" function.
# TODO: Fix the recipient object conundrum.

class HitchSMTPService(hitchserve.Service):
    def __init__(self, python=sys.executable, port=10025, needs=None, **kwargs):
        kwargs['command'] = [python, "-u", "-m", "hitchsmtp.smtp", "--port", str(port)]
        kwargs['log_line_ready_checker'] = lambda line: "SMTP Server running" in line
        super(HitchSMTPService, self).__init__(**kwargs)
