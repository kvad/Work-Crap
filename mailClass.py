#!/usr/bin/env python
#basic mail class
#Simple class for sending mail
#
#

import smtplib
class OutBoundMail:
	def __init__(self, server, subject, message, fromaddr, toaddr):
		self.server = server
		self.subject = subject
		self.message = message
		self.fromaddr = fromaddr
		self.toaddr = toaddr
		self.send_message = ""

	def prep(self):
		self.sent_message = """To: %s
From: %s
Subject: %s

%s

 """ % (",".join(self.toaddr), self.fromaddr, self.subject,self.message)
	
	def send(self):
		try:
			s = smtplib.SMTP(self.server)
			s.set_debuglevel(1)
			s.sendmail(self.fromaddr, self.toaddr, self.sent_message)
		except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException), e:
			print "*** Messages may not have been sent bro :( ***"
			print e
		#do more later 	
		

#Example!!!!!!!!!!!!!!!
#mailList = ["kur@mail.com","kurt@gmail.com"] #bulk mail baby all in one list!

#c = OutBoundMail("localhost","Fuck you","whats up gangbanger","kurtis",mailList)
#c.prep()
#c.send()
		
		
