#!/usr/bin/python

import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import datetime
import os
import logging

LOG_FILENAME = '/home/pi/log/python.out'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)

logging.debug('This message should go to the log file')

try:

	filename = sys.argv[1]
	gmail_user = "bobthesheep22@gmail.com"
	gmail_pwd = "u2421mathm50"

	now = datetime.datetime.now()

	def mail(to, subject, text, attach):
	   msg = MIMEMultipart()

	   msg['From'] = gmail_user
	   msg['To'] = to
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

	mail("bobthesheep22@gmail.com",
	        "RasPi Cam Motion detected at {}" .format(now.strftime("%I:%M%p on %B %d, %Y")),
	   "This is a email sent by a RasPi",
	   filename )

except:
   logging.exception('Got exception on main handler')
   raise
