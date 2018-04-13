from flask import g, url_for, redirect, request
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView

from wtforms import SelectField, TextAreaField

from personal_site.app import app, db
from personal_site.models import Email, Entry, Tag

from personal_site.mailing.blueprint import send_mail, generate_token

import os
import glob

class AdminAuthentication(object):
    def is_accessible(self):
        return g.user.is_authenticated

class BaseModelView(AdminAuthentication, ModelView):
    pass

class SlugModelView(BaseModelView):

    def on_model_change(self, form, model, is_created):
         model.generate_slug()
         return super(SlugModelView, self).on_model_change(form, model, is_created)

class EntryModelView(SlugModelView):

    _status_choices = [
        (Entry.STATUS_PUBLIC, 'Public'),
        (Entry.STATUS_DRAFT, 'Draft')
        ]

    '''
        We'll want to replace this later.

        Recursively get a list of filenames for use with the image selector.
    '''
    #prefix = app.config['STATIC_DIR'] + '/**/'
    _img_choices = [('', 'None')]
    _img_choices += [(filename, filename[filename.rfind('/') + 1:]) for x in os.walk(app.config['STATIC_DIR']) for filename in glob.glob(os.path.join(x[0], '*thumb*'))]

    column_choices = {
        'status': _status_choices,
        'img': _img_choices
    }

    column_list = [
        'title', 'status', 'summary', 'tag_list', 'created_timestamp'
        ]

    column_searchable_list = ['title', 'body']

    column_filters = [
        'status', 'created_timestamp'
    ]

    column_default_sort = ('id', True)

    ###############################################

    form_columns = ['title', 'summary', 'img', 'body', 'status', 'tags']

    form_args = {
        'status': {'choices': _status_choices, 'coerce': int},
        'img': {'choices': _img_choices},
    }

    form_widget_args = {
        'body': {
            'class': 'form-control span10',
            'min-width': '100%',
            'rows': 20
        },
        'summary': {
            'class': 'form-control span10',
            'rows': 10
        }
    }

    form_overrides = {
        'status': SelectField,
        'img': SelectField,
        'summary': TextAreaField
    }

    def after_model_change(self, form, model, is_created):

        if is_created:

            mailinglist = []

            for tag in model.tags:
                mailinglist = mailinglist + Email.query.filter(tag.id == Email.tag_id).all()

            if mailinglist:
                mailinglist = set(mailinglist)

                # Now actually e-mail everyone
                for address in mailinglist:
                    unsubscribe_token = generate_token(address.address, tag.tagname, 'unsubscribe')
                    unsubscribe_url = app.config['DOMAIN'].rstrip('/') + url_for('mailing.confirm_action', action='unsubscribe', token=unsubscribe_token)
                    if model.img:
                        content = '<h1>{}</h1><p><img src="{}" /></p><p>{}</p><p><a href="{}">Read more...</a></p><p style="font-size:10px">Not interested in getting more of these updates? <a href="{}">Unsubscribe</a>'.format(model.title, app.config['PRODUCTION_DOMAIN'] + '/' + model.img[ model.img.find('static'): ], model.summary, app.config['PRODUCTION_DOMAIN'] + url_for('entries.detail', slug=model.slug), unsubscribe_url)
                    else:
                        content = '<h1>{}</h1><p>{}</p><p><a href="{}">Read more...</a></p><p style="font-size:10px">Not interested in getting more of these updates? <a href="{}">Unsubscribe</a>'.format(model.title, model.summary, app.config['PRODUCTION_DOMAIN'] + url_for('entries.detail', slug=model.slug), unsubscribe_url)

                    send_mail([address.address], '{} - New Post from kelsilindblad.com'.format(model.title), content)

        return super(EntryModelView, self).after_model_change(form, model, is_created)

class TagModelView(SlugModelView):

    form_columns = ['tagname']

class EmailModelView(BaseModelView):
    pass

class BlogFileAdmin(AdminAuthentication, FileAdmin):
    pass

class IndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not (g.user.is_authenticated):
            return redirect(url_for('login', next=request.path))
        return self.render('admin/index.html')

admin = Admin(app, 'Blog Admin', index_view=IndexView())
admin.add_view(EntryModelView(Entry, db.session))
admin.add_view(TagModelView(Tag, db.session))
admin.add_view(EmailModelView(Email, db.session))
admin.add_view(BlogFileAdmin(app.config['STATIC_DIR'], '/static/', name='Static Files'))
