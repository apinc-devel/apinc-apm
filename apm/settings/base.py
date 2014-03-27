# -*- coding:utf-8 -*-
#
#   Copyright © 2013 APINC Devel Team
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# -----------------------------------------------------------------------------

import os
import sys
import apm as apm_module

# Extends context_processors
import django.conf.global_settings as DEFAULT_SETTINGS

# -----------------------------------------------------------------------------
# Django settings for apm project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# -----------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': '', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-fr'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# -----------------------------------------------------------------------------
# Calculation of directories relative to the project module location
# -----------------------------------------------------------------------------
# http://lincolnloop.com/django-best-practices/projects.html

PROJECT_DIR = os.path.dirname(os.path.realpath(apm_module.__file__))

PYTHON_BIN = os.path.dirname(sys.executable)
ve_path = os.path.dirname(os.path.dirname(os.path.dirname(PROJECT_DIR)))
# Assume that the presence of 'activate_this.py' in the python bin/
# directory means that we're running in a virtual environment.
if os.path.exists(os.path.join(PYTHON_BIN, 'activate_this.py')):
    # We're running with a virtualenv python executable.
    VAR_ROOT = os.path.join(os.path.dirname(PYTHON_BIN), 'var')
elif ve_path and os.path.exists(os.path.join(ve_path, 'bin',
        'activate_this.py')):
    # We're running in [virtualenv_root]/src/[project_name].
    VAR_ROOT = os.path.join(ve_path, 'var')
else:
    # Set the variable root to a path in the project which is
    # ignored by the repository.
    VAR_ROOT = os.path.join(PROJECT_DIR, 'var')

if not os.path.exists(VAR_ROOT):
    os.mkdir(VAR_ROOT)

# -----------------------------------------------------------------------------
# Project URLS and media settings
# -----------------------------------------------------------------------------
ROOT_URLCONF = 'apm.urls'
APPEND_SLASH = True

#SITE_PATH = os.path.dirname(os.path.dirname(PROJECT_DIR))
# FIXME http://blog.zacharyvoase.com/2010/02/03/django-project-conventions/


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(VAR_ROOT, 'static')
# http://stackoverflow.com/questions/4565935/django-staticfiles-app-help/4566907#4566907

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locale'),
)

# Make this unique, and don't share it with anybody.
# https://gist.github.com/ndarville/3452907
#SECRET_KEY = '--------------------------------------------------'

#
# Templates
# ------------------------------------------------------------------------------
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'templates'),
)

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'apm.wsgi.application'

#
# Apps, middlewares, processors and logger
# ------------------------------------------------------------------------------

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    #'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    #'django.contrib.admindocs',
    'apm.apps.manage',
    'apm.apps.members',
    'apm.apps.pages',
    'apm.apps.association',
    'apm.apps.news',
    'apm.apps.payments',
    'apm.apps.contributions',
    # third party applications
    'tinymce',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    #'apm.backends.PersonAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'apm.context_processors.base',
    'apm.context_processors.versions',
    'apm.context_processors.user_groups',
)

PASSWORD_HASHERS = DEFAULT_SETTINGS.PASSWORD_HASHERS + (
    'apm.vhffs.VhffsPasswordHasher',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# App settings
AUTH_USER_MODEL = 'members.Person'

# App pseudo-static pages
PSEUDO_STATIC_PAGES = [
	#(slug, title),
    ("homepage-organization", "homepage-organization"),
    ("homepage-services", "homepage-services"),
    ("homepage-infrastructure", "homepage-infrastructure"),
    ("about", "About page title"),
    ("legal-notice", "Legal notice and terms of use"),
    ("contact", "Contact page title"),
    ("organization", "The organization"),
    ("statutes", "Statuts de l'association"),
    ("by-laws", "Règlement intérieur"),
    ("services", "Services fournis par l'association"),
    ("sponsors", "Sponsors"),
]

# App groups
APM_GROUPS = [
	#(name, slug, email),
	("apinc-admin", "apinc-admin", "a-admin@a.a"),
    ("apinc-devel", "apinc-devel", "a-devel@a.org"),
    ("apinc-bureau", "apinc-bureau", "a-bureau@a.org"),
	("apinc-secretariat", "apinc-secretariat", "a-secretariat@a.org"),
	("apinc-tresorier", "apinc-tresorier", "a-tresorier@a.org"),
	("apinc-contributeur", "apinc-contributeur", "a-contrib@a.org"),
    #("apinc-membre", "apinc-member", "a-membre@a.org"),
]

# App roles
APM_ROLES = [
    #(name, rank),
    ("Administrateur", 10),
    ("President", 30),
    ("Vice-president", 40),
    ("Tresorier", 50),
    ("Tresorier adjoint", 60),
    ("Secretaire", 70),
    ("Secretaire adjoint", 80),
    #("Membre du bureau", 90),
    #("Membre", 100),
    #("Demandeur", 110),
]

#SITE_PATH = os.path.dirname(PROJECT_DIR)
TMP_PATH = os.path.join(VAR_ROOT, "tmp") # donnees temporaires (unused yet) 

VERSION = '0.1.0'
JQUERY_VERSION = '1.11.0'
JQUERY_UI_VERSION = '1.10.3'

PORTAL_ADMIN = 'apinc-admin'
APINC_SIREN = '448 004 556'
APINC_CNIL = '783317'
APINC_SIEGE_ADDRESS = ["APINC", "1024 rue Linus Torvald", "31000, TOULOUSE"]
APINC_SIGNATURE_TRESORIER = os.path.join(VAR_ROOT, "private/signature_tresorier.jpg")

VHFFS_REST_API_SCHEME = ''
VHFFS_REST_API_SERVER = ''
VHFFS_REST_API_PORT = ''
VHFFS_REST_API_TIMEOUT = 0.050 # seconds

VHFFS_PANEL_SUBSCRIBE_URL = "https://panel.apinc.org/?do=subscribe"
VHFFS_PANEL_LOST_PASSWORD_URL = "https://panel.apinc.org/?do=lost"

# -----------------------------------------------------------------------------
# Third party application settings
# -----------------------------------------------------------------------------
TINYMCE_JS_URL = os.path.join(STATIC_URL, 'tiny_mce/tiny_mce_src.js')
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace,inlinepopups",
    'theme': "advanced",
    'theme_advanced_buttons1' : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,formatselect,fontsizeselect,|,forecolor,backcolor,|,bullist,numlist,|,outdent,indent,|,sub,sup,|,charmap,emotions,separator,forecolor,backcolor",
    'theme_advanced_buttons2' : "pastetext,pasteword,selectall,|,undo,redo,|,link,unlink,anchor,image,code,|,tablecontrols,|,fullscreen",
    'theme_advanced_buttons3' : "",
    'relative_urls': False,
}

PAYPAL_MODE = 'sandbox' # or 'live'
PAYPAL_CLIENT_ID = ''
PAYPAL_CLIENT_SECRET = ''
