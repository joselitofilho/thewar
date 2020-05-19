#!/usr/bin/env python
# -- coding: utf-8 --

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

fromaddr = 'guerra@meutabuleiro.net'
toaddrs = ['brunomaomeh@gmail.com', 'toymak3r@gmail.com', 'joselitofilhoo@gmail.com']
subject = 'Python email'

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = subject
msg['From'] = fromaddr
msg['To'] = ', '.join(toaddrs)

# Create the body of the message (a plain-text and an HTML version).
text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
html = """\
<html>
  <head></head>
  <body>
    <b>Guerra no meu tabuleiro</b><br/><br/>
    Venha conhecer o jogo mais emocionante de guerra no tabuleiro! Jogue agora! É de graça!<br/><br/>
    <h1><a href='http://guerra.meutabuleiro.com'>http://guerra.meutabuleiro.com</a></h1><br/>
    Nos visite no <a href='https://facebook.com/guerrameutabuleiro'><img src="http://poweruser.aeiou.pt/wp-content/uploads/2013/10/facebook.png" alt="facebook" width="42" height="42"></a>
  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

# Credentials (if needed)
username = 'guerra@meutabuleiro.net'
password = 'guerra1234qwer'

# The actual mail send
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username, password)
server.sendmail(fromaddr, toaddrs, msg.as_string())
server.quit()
