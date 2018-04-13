import bcrypt
import datetime
import re

from personal_site.app import db, login_manager

@login_manager.user_loader
def _user_loader(user_id):
     return User.query.get(int(user_id))

def slugify(s):
    return re.sub('[^\w]+', '-', s).lower()

entry_tags = db.Table('entry_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'))
)

class Comment(db.Model):
    STATUS_PENDING_MODERATION = 0
    STATUS_PUBLIC = 1
    STATUS_SPAM = 8

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(254))
    ip_address = db.Column(db.String(64))
    body = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=STATUS_PUBLIC)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'))

    def __repr__(self):
        return '<Comment from {}>'.format(self.name)

class Entry(db.Model):
    STATUS_PUBLIC = 0
    STATUS_DRAFT = 1

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=STATUS_PUBLIC)
    img = db.Column(db.String(100))
    summary = db.Column(db.String(500))
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    modified_timestamp = db.Column(
        db.DateTime,
        default = datetime.datetime.now,
        onupdate = datetime.datetime.now)

    tags = db.relationship('Tag', secondary=entry_tags, backref=db.backref('entries', lazy='dynamic'))
    comments = db.relationship('Comment', backref='entry', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = ''
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Entry: {}>'.format(self.title)

    @property
    def tag_list(self):
      return ', '.join(tag.name for tag in self.tags)

    @property
    def tease(self):
        return self.body[:100]

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(64), unique=True)
    slug = db.Column(db.String(64))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = self.generate_slug()

    def generate_slug(self):
        self.slug = ''
        if self.tagname:
            self.slug = slugify(self.tagname)

    def __repr__(self):
        return '<Tag {}>'.format(self.tagname)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(254))
    tag_id = db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(255))
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64))

    def __init__(self, name, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.generate_slug()
        self.name = name

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)

    def check_password(self, raw_password):
        return bcrypt.hashpw(raw_password.encode('utf-8'), self.password_hash.encode('utf-8')) == self.password_hash.encode('utf-8')
        return False

    @staticmethod
    def authenticate(name, password):
        user = User.query.filter(User.name == name).first()
        if user and user.check_password(password):
            return User
        return False

    # Flask-Login interface
    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.is_authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
