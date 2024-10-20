from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from asgiref.sync import async_to_sync
from celery.app import Celery
from sqlalchemy import delete

from src.database import session_manager
from src.utils.tokens import JWT
from src.models.users import User
from src.models.enterprises import Enterprise
from src.config import get_settings


celery_app = Celery(__name__, broker='redis://redis:6379/0')
celery_app.autodiscover_tasks()


def send_mail(subject: str, text: str, recipient) -> None:
    settings = get_settings()
    host_user = settings.email_host_user
    host_password = settings.email_host_password

    msg = MIMEText(text, 'html')
    msg['Subject'] = subject
    msg['From'] = 'kvydyk@gmail.com'
    msg['To'] = recipient

    server = SMTP_SSL('smtp.gmail.com', 465)
    server.login(host_user, host_password)
    server.send_message(msg)
    server.quit()


@celery_app.task
def send_confirmation_letter(recipient: str, token_data: dict, url_from: str) -> str:
    token = JWT.create_token(token_data, exp_time=360)
    subject = 'Registration Confirmation'
    text = ('Confirmation link: ' \
            f'http://localhost:8000/{url_from}/register-confirm/{token}')

    send_mail(subject, text, recipient)
    return 'Ok'


@celery_app.task
def send_password_reset(recipient: str, token_data: dict) -> None:
    token = JWT.create_token(token_data)
    subject = 'Password Reset'
    text = f'http://localhost:3000/password-reset/{token}'

    send_mail(subject, text, recipient)
    return 'Ok'


@celery_app.task
def delete_inactive_user(username: str) -> None:
    async def delete_user(username: str):
        stmt = delete(User).where(User.username == username)
        async with session_manager.session() as session:
            await session.execute(stmt)
            await session.commit()
    async_to_sync(delete_user)(username)


@celery_app.task
def delete_inactive_enterprise(name: str) -> None:
    async def delete_enterprise(name: str):
        stmt = delete(Enterprise).where(Enterprise.name == name)
        async with session_manager.session() as session:
            await session.execute(stmt)
            await session.commit()
    async_to_sync(delete_enterprise)(name)
