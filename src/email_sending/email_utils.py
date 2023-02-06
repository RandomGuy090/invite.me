from threading import Thread

from flask_mail import Message

from src.config import mail, app, Email_config, lang
import random, time


class Emailer:
	
	sender = app.config.get("MAIL_SENDER")
	text_body = ""
	html_body = ""
	subject = ""
	def __init__(self):
		self.sender = app.config.get("MAIL_SENDER")
		print(f"SENDER {self.sender}")
		# self.html_template = 
		self.text_body = ""
		self.html_body = ""
		self.subject = ""

	def send_async_email(self, app, msg):
			with app.app_context():
				print("sending mail")
				try:

					msg.msgId = msg.msgId.split('@')[0] + '@invite_me_server'  
					r = random.randrange(0, 20)
					print(f"sleep {r}")
					time.sleep(r)

					mail.send(msg)
					print("mail sent")
				except Exception as e:
					print(e)


	def send_email(self, recipients):
		print(f"mail {recipients}")
		msg = Message(self.subject, 
			sender=self.sender, 
			recipients=recipients,
			extra_headers={"mailer_transport": "mail"})
		msg.body = self.text_body
		msg.html = self.html_body
		# print(msg.header)
		thr = Thread(target=self.send_async_email, args=[app, msg])
		thr.start()


class Register_email(Emailer):

	def __init__(self, form, event_name=None):	
		self.subject = lang.register
		# self.form = f"your activation link is: {self.form.email.data}" 
		self.form = form
		if event_name:
			self.subject = event_name
		else:
			self.subject = lang.declaration

	def send(self, recipients):
		# self.body =
		# self.text_body = f"your activation link is: {self.form.email.data}" 

		self.send_email(recipients)


class Code_email(Emailer):

	def __init__(self, form):	
		if event_name:
			self.subject = event_name
		else:
			self.subject = lang.declaration

		# self.form = f"your activation link is: {self.form.email.data}" 
		self.form = form

	def send(self, recipients):
		# self.body =
		# self.text_body = f"your activation link is: {self.form.email.data}" 

		self.send_email(recipients)

class Declaration_email(Emailer):

	def __init__(self, form, event_name=None):	
		if event_name:
			self.subject = event_name
		else:
			self.subject = lang.declaration
		# self.form = f"your activation link is: {self.form.email.data}" 
		self.form = form

	def send(self, recipients):
		# self.body =
		# self.text_body = f"your activation link is: {self.form.email.data}" 

		self.send_email(recipients)


class Invitation_mail(Emailer):

	def __init__(self, form, event_name=None):	
		if event_name:
			self.subject = event_name
		else:
			self.subject = lang.declaration
		# self.form = f"your activation link is: {self.form.email.data}" 
		self.form = form

	def send(self, recipients):
		# self.body =
		# self.text_body = f"your activation link is: {self.form.email.data}" 

		self.send_email(recipients)
