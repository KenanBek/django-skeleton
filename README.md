django-skeleton
===============

Skeleton for Django projects.

[![Build Status](https://travis-ci.org/KenanBek/django-skeleton.svg?branch=master)](https://travis-ci.org/KenanBek/django-skeleton)

# Features

- CKEditor with configured file upload
- Reversion
- Management commands for initial configuration
- Website model (Widget, Page, Post and Category)
- Pre configured specific folder of Django application (fixtures, media, static, etc.)
- Slider
- Email subscription
- Contact and Application database
- Logging

# Install

To install Django Skeleton on your machine run following commands:

    git clone https://github.com/KenanBek/django-skeleton.git
    cd django-skeleton/app
    pip install -r requirements.txt
    python manage.py inittest

Last command will ask you enter password for super user. Command **inittest** will create sample data. After you successfully entered required information you will be able to run application.

    python manage.py runserver

Visit **http://localhost:8000** for website, **http://localhost:8000/admin** for administration.


# Demo

Visit [Website](http://django-skeleton.bekonline.webfactional.com/) and [Admin](http://django-skeleton.bekonline.webfactional.com/admin) to try Django Skeleton on demand.

Superuser login and password:

    Login: admin
    Password: admin

# License

Licensed under GNU GPL v3.0
