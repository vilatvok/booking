from smtplib import SMTP_SSL
from email.mime.text import MIMEText

from src.application.interfaces.services.tokens import ITokenService
from src.infrastructure.config import Settings


class BackgroundTasksService:

    def __init__(self, settings: Settings):
        self.settings = settings
        self.email_host_user = settings.email_host_user
        self.email_host_password = settings.email_host_password

    def send_mail(self, subject: str, text: str, recipient: str) -> None:
        msg = MIMEText(text, 'html')
        msg['Subject'] = subject
        msg['From'] = 'kvydyk@gmail.com'
        msg['To'] = recipient

        server = SMTP_SSL('smtp.gmail.com', 465)
        server.login(self.email_host_user, self.email_host_password)
        server.send_message(msg)
        server.quit()

    def send_confirmation_letter(
        self,
        token_service: ITokenService,
        recipient: str,
        token_data: dict,
    ) -> str:
        token = token_service.encode(token_data, exp_time=360)
        subject = 'Registration Confirmation'
        text = ('Confirmation link: ' \
                f'http://localhost:8000/auth/register-confirm/{token}')

        self.send_mail(subject, text, recipient)
        return 'Ok'

    def send_password_reset(
        self,
        token_service: ITokenService,
        recipient: str,
        token_data: dict,
    ) -> str:
        token = token_service.encode(token_data)
        subject = 'Password Reset'
        text = f'http://localhost:3000/password-reset/{token}'

        self.send_mail(subject, text, recipient)
        return 'Email was sent'
