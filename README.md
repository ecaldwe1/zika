# Overview



#System requirements

This Django project has been tested on Windows 10 x64, MAC OS 10.7 and CentOS 7

* Django 1.9
* Python 2.7
* PostgreSQL 9.4
* Apache 2.4

#Quick Start Guide
1. Create database structures
    `./manage.py migrate`

2. Check if there are database migrations by reviewing the list of known migrations:
    `./manage.py migrate --list`

3. Create an admin user
   `./manage.py createsuperuser`


#Using Vagrant

1. Create Virtualbox VM `vagrant up`. It may take a while when starting VM for the first time

2. Login to VM using `vagrant ssh` command or your favorite ssh client. Login: vagrant, password vagrant

3. Switch to /vagrant directory `cd /vagrant`

4. Start django server `python manage.py runserver 0.0.0.0:8000`
Note you have to use 0.0.0.0 as server address, otherwise port forwarding may not work

You can edit files in your project directory, and changes will be visible to the virtual machine
(in /vagrant directory)

Credentials

*SSH* Login: vagrant, password vagrant

*PostgreSQL* Database: zika, Login: zika, Password: zika

*Note*: To utilize the PostgreSQL database, create a `settings_local.py` file containing the following:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'zika',
        'USER': 'zika',
        'PASSWORD': 'zika',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

# Production deployment checklist

1. Change database to PostgreSQL in settings_local.py

2. Set DEBUG to False in settings_local.py

3. Generate new SECRET_KEY
 
4. Change ALLOWED_HOSTS and ADMINS accordingly

5. Set APP_ENV to 'production'

# Enable VecNet SSO

1. Install django-auth-pubtkt package
`pip install django-auth-pubtkt`

2. Copy public key for validating pubtkt tickets to /etc/httpd/conf/sso/tkt_pubkey_dsa.pem

3. Enable DjangoAuthPubtkt middleware - put snippet below to website/settings_local.py
Order is important - if you choose to keep standard Django authentication 
backends, then django_auth_pubtkt.DjangoAuthPubtkt should be after them.
```MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django_auth_pubtkt.DjangoAuthPubtkt',
    'django.contrib.messages.middleware.MessageMiddleware',
) ```

4. Set configuration options below (in website/settings_local.py)
```from django_auth_pubtkt.views import redirect_to_sso
from django.conf.urls import url
LOGIN_URL = "/sso/"
TKT_AUTH_LOGIN_URL = "https://www.vecnet.org/index.php/sso-login"
TKT_AUTH_PUBLIC_KEY = '/etc/httpd/conf/sso/tkt_pubkey_dsa.pem'
SSO_URLS = [url(r'^sso/', redirect_to_sso),]
```


