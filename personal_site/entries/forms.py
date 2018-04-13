#from flask_wtf import FlaskForm
from wtforms import Form
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import InputRequired

from personal_site.models import Entry

class EntryForm(Form):
#class EntryForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    body = TextAreaField('Body', validators=[InputRequired()])
    status = SelectField(
        'Entry status',
        choices = (
            (Entry.STATUS_PUBLIC, 'Public'),
            (Entry.STATUS_DRAFT, 'Draft')),
        coerce=int,
        validators=[InputRequired()])
     

    def save_entry(self, entry):
        self.populate_obj(entry)
        entry.generate_slug()
        return entry
