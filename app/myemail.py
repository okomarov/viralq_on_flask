from threading import Thread

from flask import current_app
from flask import render_template
from flask_mail import Message

from app import utils
from app.extensions import mail


def _send_async(app, msg):
    with app.app_context():
        mail.send(msg)


def send(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=_send_async,
           args=(current_app._get_current_object(), msg)).start()


def send_from_default(subject, recipients, text_body, html_body):
    send(subject,
         current_app._get_current_object().config['MAIL_USERNAME'],
         recipients, text_body, html_body)


def send_verification_email(user_id, user_email, referring_uuid=''):
    payload = {
        'user_id': user_id,
        'referring_uuid': referring_uuid}
    jwt_token = utils.encode_jwt_token(payload)
    send_from_default(subject='Please verify your email address',
                      recipients=[user_email],
                      text_body=render_template(
                          'email/verify_email.txt', token=jwt_token),
                      html_body=render_template(
                          'email/verify_email.html', token=jwt_token))
