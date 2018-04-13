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
* If you want to use the mailing list features, set `EMAIL_ENABLED = True` and fill out the SMTP variables with the appropriate values for your mailserver

To run a local instance for testing:

    python manage.py runserver

By default you can view your new site at `http://localhost:5000`
