import smtplib
 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email_core():
	def __init__(self, app):
		self.app = app
		
		username = 'username'
		password = 'password'
		

 
	def send(self, message):
		msg_form = MIMEMultipart('mixed')

		print(f"send message {message}")

		self.s = smtplib.SMTP(self.app.config.get("MAIL_SERVER"), self.app.config.get("MAIL_PORT"))
		self.s.starttls()
		self.s.login(self.app.config.get("MAIL_USERNAME"),self.app.config.get("MAIL_PASSWORD"))
		
		
		message = MIMEText(message, "html")
		self.msg_form.attach(message)
		try:
			print("self.recipient")
			print(self.recipient)
			print(self.recipient)
			for recip in self.recipient:
				self.s.sendmail(recip, self.app.config['MAIL_SENDER'], msg_form.as_string())
		finally:
			self.s.quit()

class Message():
	subject = ""
	sender = ""
	recipients = ""

	def __init__(self, *args, **kwargs):
		self.subject = kwargs.get("subject") if kwargs.get("subject") else "Subject"
		self.recipients = kwargs.get("recipients") if kwargs.get("recipients") else "recipients"
		self.sender = kwargs.get("sender") if kwargs.get("sender") else "sender"

		print(f"email_core, {self.subject},{self.recipients} ")

		msg = MIMEMultipart('mixed')

		msg['Subject'] = self.subject
		msg['From']    = self.sender
		msg['To']      = self.recipients

	def __str__(self):
		print(self.html)
		return self.html

	def encode(self, *args, **kwargs):
		return str(self)

		