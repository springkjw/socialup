import os

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')

SECRET_KEY = '_f^=by$nf^gjb2+o*e)nz+&%_^ykb&ro(rd$fh#o_8443z7!cv'

DEFAULT_SITE_ID = 1

# send email setting
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.naver.com'
DEFAULT_FROM_EMAIL = 'social_up@naver.com'
EMAIL_HOST_USER = 'social_up@naver.com'
EMAIL_MAIN = 'social_up@naver.com '
EMAIL_HOST_PASSWORD = 'qwqw1212!!'
EMAIL_PORT = 587

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'accounts',
    'markets',
    'reviews',
    'billing',
    'carts',
    'contact',
    'report',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'django_summernote',
]

# custom middleware
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'socialup.middleware.SiteMiddleware',
    # 'socialup.middleware.LoginRequireMiddleware',
]

# except urls
LOGIN_EXECPT_URLS = (
    r'^$',
    r'^admin/',
    r'^accounts/signup/',
    r'^/accounts/facebook/login/?process=login',
)

ROOT_URLCONF = 'socialup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'socialup.wsgi.application'

# all-auth setting
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_ADAPTER = 'accounts.adapter.AccountAdapter'
ACCOUNT_FORMS = {
    'signup': 'accounts.forms.SignupForm',
    'login': 'accounts.forms.LoginForm',
    'reset_password': 'accounts.forms.ResetPasswordForm',
    'reset_password_from_key': 'accounts.forms.ResetPasswordKeyForm',
}

# all-auth social account setting
SOCIALACCOUNT_ADAPTER = 'accounts.adapter.SocialAccountAdapter'
SOCIALACCOUNT_PROVIDERS = \
    {'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', ],
        'AUTH_PARAMS': {'auth_type': 'https'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time'],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': True,
        'VERSION': 'v2.4'
    }
    }

AUTH_USER_MODEL = 'accounts.MyUser'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# language & time setting
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'ROK'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# iamport setting
IAMPORT_KEY = '9174285101672135'
IAMPORT_SECRET = '72tZp9MnizPwplFrwjbKszi9o0QF8pKgsegSo2fGC5c2rStXbFIEf0OD0Ei943qwhGpGJEmlKzobrS9D'

# sendbird setting
SD_API_ID = '68C1D6E3-BFC1-4B8E-B11C-6B1FBE0D3AAA'
SD_API_TOKEN = 'ce9c13eb2b734ab9749711d122f67e478b618552'
