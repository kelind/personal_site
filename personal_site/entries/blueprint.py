from flask import Blueprint, redirect, request, url_for
from flask_mako import render_template

from sqlalchemy import func

from personal_site.helpers import object_list
from personal_site.models import Entry, Tag

from personal_site.forms import CommentForm

from personal_site.entries.forms import EntryForm

entries = Blueprint('entries', __name__, template_folder='templates')

'''
@entries.route('/create/', methods=['GET', 'POST'])
def create():

    from app import db

    if request.method == 'POST':
        form = EntryForm(request.form)
        if form.validate():
            entry = form.save_entry(Entry())
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('entries.detail', slug=entry.slug))
    else:
        form = EntryForm()

    return render_template('create.mak', form=form)
'''

@entries.route('/')
def index():
    entries = Entry.query.filter(Entry.status == Entry.STATUS_PUBLIC).order_by(Entry.created_timestamp.desc())
    return object_list('main.mak', entries, page_title='Home')

@entries.route('/tags/')
def tag_index():

    from personal_site.app import db 

    tags = db.session.query(Tag.tagname, Tag.slug, func.count(Tag.tagname)).group_by(Tag.tagname).order_by(Tag.tagname).all()

    return render_template('tags.mak', tags=tags)

@entries.route('/tags/<slug>')
def tag_details(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    entries = tag.entries.filter(Entry.status == Entry.STATUS_PUBLIC).order_by(Entry.created_timestamp.desc())
    return object_list('main.mak', entries, tag=tag, page_title='Entries Tagged {}'.format(tag.tagname))

@entries.route('/<slug>/')
def detail(slug):
    entry = Entry.query.filter((Entry.slug == slug) & (Entry.status == Entry.STATUS_PUBLIC)).first_or_404()
    form = CommentForm(data={'entry_id': entry.id})
    resources = ['comments.js']
    return render_template('entry.mak', entry=entry, form=form, resources=resources)
