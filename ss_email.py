import sys, os
import numpy as np
import copy
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from sendgrid import SendGridAPIClient
class EmailService:
	def __init__(self):
		pass

	def send(self, player):

		name = player['name']
		email = player['email']
		secret_santa = player['secret_santa']
		ss_wishlist = player['ss_wishlist']

		body = f'''
		Hi {name}
		<br>
		<br>
		Your secret santa is <strong>{secret_santa}</strong>.
		<br>
		<br>
		You can find <strong>{secret_santa}'s</strong> wishlist <a href="{ss_wishlist}">here</a>
		<br>
		<br>
		'''
		message = Mail(
				from_email='noreply@secretsanta.com',
				to_emails=email,
				subject=f'Secret Santa Selection',
				html_content=body
				)
		try:

			key = os.environ.get('SENDGRID_API_KEY')
			sg = SendGridAPIClient(key)
			response = sg.send(message)
			print('sending email to', name)
		except:
			traceback.print_exc()

