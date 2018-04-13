from wtforms import Form, PasswordField, BooleanField, HiddenField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from personal_site.models import Entry, User

class CommentForm(Form):
    name = StringField('Name: ', validators=[DataRequired(), Length(1, 64, 'Names cannot exceed 64 characters in length.')])
    email = StringField('Email: ', validators=[Email()])
    body = TextAreaField('Comment: ', validators=[DataRequired(), Length(10, 3000, 'Comments must be at least 10 and no more than 3,000 characters long.')])
    entry_id = HiddenField(validators=[DataRequired()])

    def validate(self):
        if not super(CommentForm, self).validate():
            return False

        # Ensure that entry_id maps to a public entry
        entry = Entry.query.filter(
            (Entry.status == Entry.STATUS_PUBLIC) &
            (Entry.id == self.entry_id.dat)).first()
        
        if not entry:
            return False
        else:
            return True

class LoginForm(Form):
    name = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    remember_me = BooleanField("Remember me?", default=True)

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        self.user = User.authenticate(self.name.data, self.password.data)
        if not self.user:
            self.name.errors.append("Invalid email or password.")
            return False

        return True
