#!/usr/bin/env python
# -- coding: utf-8 --

import smtplib

fromaddr = 'guerra@meutabuleiro.net'
toaddrs = ['1lucasmf@gmail.com', 'joselitofilhoo@gmail.com', 'katryne@meutabuleiro.net']
subject = 'Email teste'

hdr = "From: %s\r\nTo: %s\r\nSubject: %s\r\nX-Mailer: My-Mail\r\n\r\n" % (fromaddr, toaddrs, subject)
msg = 'Foi gerado uma senha temporária para você. Entre no jogo para alterá-la. Obrigado.'

# Credentials (if needed)
username = 'guerra@meutabuleiro.net'
password = 'guerra1234qwer'

# The actual mail send
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username, password)
server.sendmail(fromaddr, toaddrs, hdr + msg)
server.quit()
