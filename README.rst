HitchSMTP
=========

Mock SMTP server that logs all incoming messages to stdout as JSON for easy parsing
by HitchServe_.

HitchSMTP contains a service definition for use with Hitch, but can
also be used alone.


Use with Hitch
==============

Install like so::

    $ hitch install hitchsmtp


.. code-block:: python

        # Service definition in your test execution engine's setUp
        self.services['HitchSMTP'] = hitchsmtp.Service()

        # Wait for email during test
        self.services['HitchSMTP'].logs.out.tail.until_json(
            lambda email: containing in email['payload'],
            timeout=5,
            lines_back=1,
        )


See this service in action at the DjangoRemindMe_ project.


Features
========

* Logs all details about emails received by the SMTP server as easily parsed JSON.
* Parses links in your emails automatically so that you can check just for links in emails.
* Can also mock the effect of SMTP errors.


Bad SMTP Server
===============

You can send to specific email addresses to mock most SMTP errors.

E.g. Sending an email to 451-please-try-again-later@smtperrors.com will cause the "451 Please try again later" SMTP error.

For a full list of these errors and the email address that triggers them, see:

https://github.com/crdoconnor/hitchsmtp/blob/master/hitchsmtp/smtperrors.py


.. _DjangoRemindMe: https://github.com/crdoconnor/django-remindme

.. _HitchServe: https://github.com/crdoconnor/hitchserve
