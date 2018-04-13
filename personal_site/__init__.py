from personal_site.app import app
import personal_site.admin
import personal_site.models
import personal_site.views

from personal_site.entries.blueprint import entries
from personal_site.mailing.blueprint import mailing

app.register_blueprint(entries, url_prefix='/entries')
app.register_blueprint(mailing, url_prefix='/mailing')

if __name__ == '__main__':
    app.run()
