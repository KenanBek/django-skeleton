django-skeleton
===============

Skeleton for Django projects.

Current version: 1.0.0 (ongoing).

[![Build Status](https://travis-ci.org/KenanBek/django-skeleton.svg?branch=master)](https://travis-ci.org/KenanBek/django-skeleton)

[![Coverage Status](https://img.shields.io/coveralls/KenanBek/django-skeleton.svg)](https://coveralls.io/r/KenanBek/django-skeleton)

# Features

## Version 1.x.x

- Cart application
    - Product and Shop entities
    - Product filter
    - Different price for each Shop
    - Product and Shop user review (5 star rating system)
    - Shop news
    - Product's image and video
- Custom user authentication with user profile
- Multiple form support
- Import and Export to most popular file formats (xml, csv, etc.)
- Auto select for administration (Django Select2)
- CKEditor with configured file upload
- Model history and reversion (possibility to back to old versions of the model)
- Management commands for initial configuration
- Website model (Widget, Page, Post and Category)
- Customized Django Suit based administration
- Pre configured specific folders of Django application (fixtures, media, static, etc.)
- Slider
- Email subscription
- Contact and Application database
- Logging

# Install

To install Django Skeleton on your machine run following commands:

    git clone https://github.com/KenanBek/django-skeleton.git
    cd django-skeleton/app
    pip install -r requirements.txt
    python manage.py inittestdata

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
