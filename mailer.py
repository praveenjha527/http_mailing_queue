import smtplib
import time
import os
import logging
import sys
import configparser

logger = logging.getLogger(__name__)

def mailer_service(q, queue_delay, logs_directory, file_conf):

    logger.setLevel(logging.INFO)

    if not logs_directory:
        logger.addHandler(logging.StreamHandler(sys.stdout))
    else:
        log_path = os.path.join(args.logs_directory, "mailer.log")
        logger.addHandler(logging.FileHandler(log_path))
    # Handling File based configuration
    if file_conf:
        config = configparser.ConfigParser()
        config.read(file_conf)
        SMTP_SEVER = config['MAIL_CONF']['MAIL_SERVER']
        SMTP_PORT = config['MAIL_CONF']['ALERT_EMAIL_PORT']
        AUTH_USER = config['MAIL_CONF']['ALERT_EMAIL']
        AUTH_PASSWORD = config['MAIL_CONF']['ALERT_PASSWORD']
    else:
        SMTP_SERVER = os.environ.get('MAIL_SERVER')
        SMTP_PORT = os.environ.get('ALERT_EMAIL_PORT')
        AUTH_USER = os.environ.get('ALERT_EMAIL')
        AUTH_PASSWORD = os.environ.get('ALERT_PASSWORD')

    conn = smtplib.SMTP("{server}:{port}".format(server=SMTP_SERVER, port=SMTP_PORT))
    conn.starttls()
    conn.login(AUTH_USER, AUTH_PASSWORD)

    while 1:
        mail_data = q.get()
        if not mail_data:
            time.sleep(queue_delay)
            continue

        logger.info(mail_data)

        sender = mail_data['sender']
        receivers = mail_data['receivers']
        content = mail_data['content']
        job_id = mail_data['id']

        try:
            conn.sendmail(sender, receivers, content)
        except smtplib.SMTPServerDisconnected as e:
            q.put(mail_data)
            conn = smtplib.SMTP("{server}:{port}".format(server=SMTP_SERVER, port=SMTP_PORT))
            conn.starttls()
            conn.login(SMTP_USER, AUTH_PASSWORD)
            time.sleep(queue_delay)
            continue

        time.sleep(queue_delay)
