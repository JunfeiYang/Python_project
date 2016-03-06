#!/usr/bin/env python

#
formAddress = 'sender@example.com'
toAddress = 'me@my.domain'
msg = "Subject: Hello\n\n This is test mail"
import smtplib
server = smtplib.SMTP("localhost",25)
server.sendmail(formAddress,toAddress,msg)
{}
