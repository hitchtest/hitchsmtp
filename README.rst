HitchSMTP
=========

Mock SMTP server that logs all incoming messages to stdout as JSON for
easy parsing by HitchServe_.

HitchSMTP contains a service definition for use with Hitch, but can
also be used alone.


Use with Hitch
==============

Install like so::

    $ hitch install hitchsmtp


.. code-block:: python

        # Service definition in your test execution engine's setUp
        self.services['HitchSMTP'] = hitchsmtp.HitchSMTPService(
            port=10025                                                 # Optional (default: 10025)
        )

        # Wait for email during test...
        containing = "Registration email"

        email = self.services['HitchSMTP'].logs.out.tail.until_json(
            lambda email: containing in email['payload'] or containing in email['Subject'],
            timeout=5,
            lines_back=1,
        )


See this service in action at the DjangoRemindMe_ project.

Bad SMTP Server
===============

You can send to specific email addresses to mock most SMTP errors.

E.g. Sending an email to 451-please-try-again-later@smtperrors.com will cause the "451 Please try again later" SMTP error.

For a full list of these errors and the email address @ smtperrors.com that will trigger them, see:

https://github.com/hitchtest/hitchsmtp/blob/master/hitchsmtp/smtperrors.py

Features
========

* Logs all details about emails received by the SMTP server as easily parsed JSON.
* Parses links in your emails automatically so that you can check just for links in emails and 'click' on them.
* Can also mock SMTP errors.


.. _DjangoRemindMe: https://github.com/hitchtest/django-remindme
.. _HitchServe: https://github.com/hitchtest/hitchserve
