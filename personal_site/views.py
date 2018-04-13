from flask import url_for, flash, redirect, request
from flask_login import login_user, logout_user
from flask_mako import render_template

from personal_site.app import app
from personal_site.app import login_manager
from personal_site.forms import LoginForm
from personal_site.models import User

@app.context_processor
def date_formatter():

    def format_date(datestamp):
        import datetime

        return datetime.datetime.strftime(datestamp, '%B %d %Y')

    return dict(format_date=format_date)

@app.route('/')
def homepage():
    return redirect(url_for('entries.index'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)

        if form.validate():
            login_user(User.query.filter_by(name=form.name.data).first(), remember=form.remember_me.data)
            flash('Successfully logged in as {}'.format(form.name.data, 'Success'))

            next_url = request.args.get('next')

            if next_url:
                return redirect(next_url)
            else:
                return redirect(url_for('homepage'))

    else:
        form = LoginForm()

    return render_template('login.mak', form=form)

@app.route('/logout/')
def logout():
  logout_user()
  flash('You have been logged out.', 'Success')
  return redirect(request.arg.get('next') or url_for('homepage'))
