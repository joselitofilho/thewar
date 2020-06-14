# -*- coding: utf-8 -*-

import re
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from os.path import basename


class Email(object):
    def send_mail(self, send_from, password, send_to, subject, text, files=None, server="127.0.0.1", port=587):
        assert isinstance(send_to, list)

        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(text, 'html'))

        if files:
            for f in files or []:
                with open(f, "rb") as fil:
                    part = MIMEApplication(
                        fil.read(),
                        Name=basename(f)
                    )
                # After the file is closed
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                msg.attach(part)

        server = smtplib.SMTP(server, port)
        server.starttls()
        server.login(send_from, password)
        server.sendmail(send_from, send_to, msg.as_string())
        server.close()

    def is_valid(self, email):
        return re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email)
