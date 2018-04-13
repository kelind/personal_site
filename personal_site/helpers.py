from flask import request
from flask.ext.mako import render_template

from itsdangerous import URLSafeTimedSerializer

from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
from email.header import Header

import personal_site.app

def object_list(template_name, query, paginate_by=20, **context):
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    object_list = query.paginate(page, paginate_by)
    return render_template(template_name, object_list=object_list, **context)

def send_mail(recipients, subject, content):
    '''
        Given a set of recipients, send each an e-mail
        with subject "subject" and the specified "content." 
    '''

    from smtplib import SMTP_SSL as SMTP
    from email.mime.text import MIMEText
    from email.header import Header

    from app import config

    email_msg = MIMEText(content, 'html', 'utf-8')
    email_msg['Subject'] = Header(subject, 'utf-8')
    email_msg['From'] = 'kelsi@kelsilindblad.com'

    if len(recipients) == 1:
        email_msg['To'] = recipients[0]
        recips = [email_msg['To']]

    else:
        # We're gonna BCC everyone
        recips = list(recipients)

    s = SMTP(config['SMTP_HOST'])
    s.set_debuglevel(False)
    s.login(config['SMTP_USERNAME'], config['SMTP_PASSWORD'])

    try:
        s.sendmail(email_msg['From'], recips, email_msg.as_string())

    except:
        return False

    finally:
        s.close()
        return True

def generate_token(email, tag, action):

    import personal_site.app.config

    serializer = URLSafeTimedSerializer(config['SECRET_KEY'])

    return serializer.dumps([email, tag], salt=action)
