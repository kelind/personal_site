'''
    Okay, here's how it should work.

    You should be able to go to a URL like /mailing/subscribe/$tagname in order to sign up to receive notifications when a new post is made in that tag.

    Whenever a new post is made, its tags should be checked. For each tag, get all subscribed e-mail addresses. Then make a set() to remove duplicates and BCC everybody in that post with the post content.

   There should also be an "unsubscribe" view that will let someone remove their e-mail from the list at any time.
'''

from flask import Blueprint, redirect, request, url_for
from flask_mako import render_template

from itsdangerous import URLSafeTimedSerializer

from personal_site import app
from personal_site.models import Tag, Email

from personal_site.mailing.forms import MailingSubscribeForm

mailing = Blueprint('mailing', __name__, template_folder='templates')

def generate_token(email, tag, action):

    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    return serializer.dumps([email, tag], salt=action)

def send_mail(recipients, subject, content):
    '''
        Given a set of recipients, send each an e-mail
        with subject "subject" and the specified "content." 
    '''

    from smtplib import SMTP
    from email.mime.text import MIMEText
    from email.header import Header

    email_msg = MIMEText(content, 'html', 'utf-8')
    email_msg['Subject'] = Header(subject, 'utf-8')
    email_msg['From'] = 'kelsi@kelsilindblad.com'

    if len(recipients) == 1:
        email_msg['To'] = recipients[0]
        recips = [email_msg['To']]

    else:
        # We're gonna BCC everyone
        recips = list(recipients)

    s = SMTP(app.config['SMTP_HOST'])
    s.set_debuglevel(False)

    try:
         s.sendmail(email_msg['From'], recips, email_msg.as_string())

    except:
        return False

    finally:
        s.close()
        return True

@mailing.route('/subscribe/<slug>', methods=['GET', 'POST'])
def subscribe(slug):

    # If e-mail is turned off, you should not be here!
    if not app.config['EMAIL_ENABLED']: 
        return render_template('confirm_failed.mak', reason='disabled')

    tag = Tag.query.filter(Tag.slug == slug).first_or_404()

    if request.method == 'POST':
        form = MailingSubscribeForm(request.form)

        if form.validate():

            # Generate confirmation token and URL
            confirm_token = generate_token(form.email.data, tag.tagname, 'subscribe')
            confirm_url = request.url_root.rstrip('/') + url_for('mailing.confirm_action', action='subscribe', token=confirm_token)

            # Send confirmation e-mail, display confirmation message
            confirm_message = '<p>You are receiving this e-mail because you signed up to receive email updates from kelsilindblad.com. To confirm your interest, please click the link below to complete your registration.<p><p><a href="{}">{}</a></p>'.format(confirm_url, confirm_url)
            send_mail([form.email.data], 'kelsilindblad.com Mailing List Confirmation', confirm_message)

            return render_template('subscribe_confirm.mak', email=form.email.data)

    else:
        form = MailingSubscribeForm()

    return render_template('subscribe.mak', tag=tag, form=form)

@mailing.route('/confirm/<action>/<token>')
def confirm_action(action, token):

    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    try:
        email, tag = serializer.loads(token, salt=action, max_age=app.config['TOKEN_EXPIRATION'])

    except:
        return render_template('confirm_failed.mak', reason='other')

    # Add or remove db info

    from personal_site.app import db

    if action == 'subscribe':

        # Do not allow subscriptions if e-mail is currently disabled
        if not app.config['EMAIL_ENABLED']: 
            return render_template('confirm_failed.mak', reason='disabled')

        tag_info = Tag.query.filter(Tag.tagname == tag).first_or_404()
        entry = Email(address=email, tag_id=tag_info.id)
        db.session.add(entry)
        db.session.commit()

    elif action == 'unsubscribe':

        tag_info = Tag.query.filter(Tag.tagname == tag).first_or_404()
        deletion = Email.query.filter(Email.address == email).filter(Email.tag_id == tag_info.id).first_or_404()
        db.session.delete(deletion)
        db.session.commit()

    return render_template('confirm_succeeded.mak', action=action, tag=tag)
