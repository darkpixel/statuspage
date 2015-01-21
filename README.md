statuspage
==========

A simple self-hosted open source status page site written in Django

Inspired by [Cachet](https://github.com/cachethq/Cachet)

Cachet is a great product, I simply despise PHP.


Please file an issue if you have trouble or want to suggest an improvement!  We love to help!
https://github.com/darkpixel/statuspage/issues


Quick Setup
===========

Heroku / Dokku
--------------
* Check out the code from github
* Push it to Dokku or Heroku
* Set the DATABASE_URL variable as appropriate
* Set the variable PRODUCTION to 'True'
* Optionally set the STATUS_LOGO_URL to the logo you would like displayed on the status page
* Optionally Set the STATUS_TICKET_URL to the URL of your ticket system
* Optionally Set the STATUS_TITLE variable to something appropriate for the page title
* Optionally set the LOGO_URL to the logo you would like displayed on the status page
* Optionally Set the TICKET_URL to the URL of your ticket system
* Make sure you run: python manage.py migrate


uWSGI
-----

* Check out the code from github into a directory on your server.
* For this example we assume the code is checked out to '/var/hosting/unconfigured.org/statuspage'
* Create a virtualenv: virtualenv /var/hosting/unconfigured.org/virtualenv
* Activate the virtualenv: . /var/hosting/unconfigured.org/virtualenv/bin/activate
* Install the requirements: pip install -r /var/hosting/unconfigured.org/statuspage/requirements.txt
* The following should be sufficient as a UWSGI config:
* Make sure you run: python manage.py migrate

```
[uwsgi]
plugins=python
chdir=/var/hosting/unconfigured.org/statuspage
module=statuspage.wsgi:application
socket=127.0.0.1:9000
env=PRODUCTION=True
env=DJANGO_SETTINGS_MODULE=statuspage.settings
env=DATABASE_URL=sqlite:////var/hosting/unconfigured.org/statuspage.db
home=/var/hosting/unconfigured.org/virtualenv
uid=statuspage
gid=statuspage
```

Locally using virtualenvwrapper
-------------------------------
* mkvirtualenv statuspage
* edit ~/.virtualenvs/statuspage/bin/postactivate to export DATABASE_URL, and optionally STATUS_LOGO_URL, STATUS_TICKET_URL, and STATUS_TITLE
* Check out the code from github
* pip install -r requirements.txt
* python manage.py migrate
* python manage.py runserver
    
