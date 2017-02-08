# -*- coding: utf-8 -*-
from .base import os, BASE_DIR, INSTALLED_APPS
import raven

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ebdb',
        'USER': 'ebroot',
        'PASSWORD': 'wodnjs2010Dbwls1804',
        'HOST': 'aa82r04ezpe9o4.chhv3epwywiz.ap-northeast-2.rds.amazonaws.com',
        'PORT': 3306,
    }
}

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

AWS_ACCESS_KEY_ID = 'AKIAIQ2DFL37RSVEDTAA'
AWS_SECRET_ACCESS_KEY = '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'

AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = False
AWS_QUERYSTRING_AUTH = False

DEFAULT_FILE_STORAGE = 'socialup.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'socialup.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'snssocialup'
S3DIRECT_REGION = 'ap-northeast-2'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = 'https://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

AWS_S3_HOST = 's3.%s.amazonaws.com' % S3DIRECT_REGION

import datetime

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = {
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()),),
}


def static_url(url):
    return os.path.join(STATIC_URL, url)


SUMMERNOTE_CONFIG = {
    'iframe': True,
    'width': '100%',
    'lang': 'ko-KR',
    'attachment_require_authentication': True,
    'default_css': (
        '/static/css/bootstrap.min.css',
        static_url('django_summernote/summernote.css'),
        static_url('django_summernote/django_summernote.css'),
    ),
    'default_js': (
        '/static/js/jquery-2.2.4.min.js',
        '/static/js/bootstrap.min.js',
        static_url('django_summernote/jquery.ui.widget.js'),
        static_url('django_summernote/jquery.iframe-transport.js'),
        static_url('django_summernote/jquery.fileupload.js'),
        static_url('django_summernote/summernote.min.js'),
    ),
}

INSTALLED_APPS += ['raven.contrib.django.raven_compat', ]

# sentry settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'INFO',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'INFO',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

RAVEN_CONFIG = {
    'dsn': 'https://39c4c5642dae45a9a7bb5ade5234bda7:cd3ea0be19f64a8a917692d16d305a39@sentry.io/134317',
}
