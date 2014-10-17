django-skeleton
===============

Skeleton project for Django applications.

[![Build Status](https://travis-ci.org/KenanBek/django-skeleton.svg?branch=master)](https://travis-ci.org/KenanBek/django-skeleton) [![Coverage Status](https://coveralls.io/repos/KenanBek/django-skeleton/badge.png?branch=master)](https://coveralls.io/r/KenanBek/django-skeleton?branch=master)

# Features

**Built in applications**:

- Cart application
    - Product and Shop entities
    - Product filter
    - Different price for each Shop
    - Product and Shop user review (5 star rating system)
    - Shop news
    - Product's image and video
- Website aplications
    - Widgets
    - Static pages
    - Posts
    - Post categories
    - Slider
    - Website API

**Pre configured 3rd party packages:**

- REST Framework
- Guardian (object based permissions)
- Import Export (Import and Export to and from most popular file formats such as xml, csv, etc.)
- CKEditor (also configured to support file upload)
- Django Select2 (Auto select for administration)

**Pre configured Python/Django features:**

- Custom user authentication with user profile
- Multiple form support
- Model history and reversion (possibility to back to old versions of the model)
- Management commands for initial configuration
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
