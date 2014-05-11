#!/usr/bin/python

import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import datetime
import os
import base64
import logging

filename = sys.argv[1]
recipients_option = sys.argv[2]
cc = ""

with open('/usr/local/gmail', 'r') as f:
	gmail_pwd = f.read()
f.closed

if recipients_option == "a":
	recipients = ['bobthesheep22@gmail.com ', 'dc_cn@yahoo.com']
	
elif recipients_option == "r":
	recipients = "bobthesheep22@gmail.com"

elif recipients_option == "z":
	recipients = "dc_cn@yahoo.com"

gmail_user = "bobthesheep22@gmail.com"
gmail_pwd = base64.b64decode(gmail_pwd)

now = datetime.datetime.now()

def mail(to, subject, text, attach):
	msg = MIMEMultipart()

	msg['From'] = gmail_user

	if recipients_option == "a":
		msg['To'] = ", ". join(recipients) 
	elif recipients_option == "r":
		msg['To'] = recipients
	msg['Cc'] = cc
	msg['Subject'] = subject


	msg.attach(MIMEText(text))

	part = MIMEBase('application', 'octet-stream')
	part.set_payload(open(attach, 'rb').read())
	Encoders.encode_base64(part)
	part.add_header('Content-Disposition',
	   'attachment; filename="%s"' % os.path.basename(attach))
    	msg.attach(part)

	mailServer = smtplib.SMTP("smtp.gmail.com", 587)
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login(gmail_user, gmail_pwd)
	mailServer.sendmail(gmail_user, to, msg.as_string())
	# Should be mailServer.quit(), but that crashes...
	mailServer.close()

mail(recipients,
	"RasPi Cam Motion detected at {}" .format(now.strftime("%I:%M%p on %B %d, %Y")),
	"This is a email sent by a RasPi",
	filename )

