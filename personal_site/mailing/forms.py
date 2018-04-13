from wtforms import Form
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

class MailingSubscribeForm(Form):
    email = EmailField('Email address', [DataRequired(), Email()])
