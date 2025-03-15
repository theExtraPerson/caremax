import logging
from threading import Thread
from flask import current_app, render_template
from . import mail
from flask_mail import Message

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            logging.info('Email sent successfully')
        except Exception as e:
            logging.error(f'Error sending email: {e}')

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['RDC_MAIL_SUBJECT_PREFIX'] + subject,
            sender=app.config['RDC_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(f'{template}.txt', **kwargs)
    msg.html = render_template(f'{template}.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr