# personal_site
Code to run my personal web site

Installation
===

Clone the repository to get the source code.

    git clone https://github.com/kelind/personal_site.git

Set up a virtualenv to isolate the app's code, then install the required dependencies.

    cd personal_site
    virtualenv venv
    source venv/bin/activate
    pip install -r local-requirements.txt

Create a `config.py` to define the app's root directory, database location, etc. The file `config_template.py` contains the necessary variables with reasonable defaults.

    cp config_template.py config.py

For production, there are some settings you'll want to change:

* Set `DEBUG = False`
* Choose an actually-secret `SECRET_KEY`
* If you want to use the mailing list features, set `EMAIL_ENABLED = True` and fill out the SMTP variables with the appropriate values for your mailserver. The way the code is set up is appropriate for a server running on localhost, but does not support logging into an external server or establishing an SSL connection.

Create the database:

    python manage.py db migrate
    python manage.py db upgrade

To run a local instance for testing:

    python manage.py runserver

By default you can view your new site at `http://localhost:5000`

Be ready for a weird-looking result! The layout isn't too happy when there aren't any blog entries to retrieve.
