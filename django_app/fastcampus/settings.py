import json
import os

# Debug check
DEBUG = True
if 'RDS_HOSTNAME' in os.environ or 'EB_IS_COMMAND_LEADER' in os.environ or 'AWS_ELB_HOME' in os.environ:
    DEBUG = False
STATIC_S3 = False

# Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_DIR = os.path.join(BASE_DIR, '.conf')
SETTING_DIR = os.path.join(BASE_DIR, 'fastcampus')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# Read config file
if DEBUG:
    config = json.loads(open(os.path.join(CONF_DIR, 'settings_debug.json')).read())
else:
    config = json.loads(open(os.path.join(CONF_DIR, 'settings_deploy.json')).read())

# Staticfiles
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    STATIC_DIR,
)
STATIC_ROOT = os.path.join(BASE_DIR, '../static_root')

# django-compressor
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_PRECOMPILERS = (
    ('text/x-sass', 'sass {infile} {outfile}'),
)


# AWS
if not DEBUG or STATIC_S3:
    AWS_HEADERS = {
        'Expires': 'Thu, 31 Dec 2199 20:00:00 GMT',
        'Cache-Control': 'max-age=94608000',
    }
    AWS_STORAGE_BUCKET_NAME = config['aws']['AWS_STORAGE_BUCKET_NAME']
    AWS_ACCESS_KEY_ID = config['aws']['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = config['aws']['AWS_SECRET_ACCESS_KEY']
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

    STATICFILES_LOCATION = 'static'
    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
    STATICFILES_STORAGE = 'fastcampus.custom_storages.StaticStorage'

    MEDIAFILES_LOCATION = 'media'
    MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
    DEFAULT_FILE_STORAGE = 'fastcampus.custom_storages.MediaStorage'

    COMPRESS_URL = STATIC_URL
    COMPRESS_STORAGE = STATICFILES_STORAGE
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

# Auth
AUTH_USER_MODEL = 'member.MyUser'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'member.backends.FacebookBackend',
]
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

# Facebook
FACEBOOK_APP_ID = config['facebook']['FACEBOOK_APP_ID']
FACEBOOK_SECRET_CODE = config['facebook']['FACEBOOK_SECRET_CODE']
FACEBOOK_APP_ACCESS_TOKEN = '%s|%s' % (FACEBOOK_APP_ID, FACEBOOK_SECRET_CODE)


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'storages',
    'compressor',

    'course',
    'member',
    'projects.blog',
    'projects.video',
    'projects.sns',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATE_DIR,
        ],
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


# Databases
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = config['databases']

# Log
DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

# Secure
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Email
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config['email']['EMAIL_HOST']
EMAIL_PORT = config['email']['EMAIL_PORT']
EMAIL_HOST_USER = config['email']['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = config['email']['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = config['email']['EMAIL_USE_TLS']
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Other settings
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

ROOT_URLCONF = 'fastcampus.urls'
WSGI_APPLICATION = 'fastcampus.wsgi.application'
SECRET_KEY = 'u*8!!mqh10rzxgdom1&1y%x1d&-8!$sd*#_lr9&n5mp5+nh_jy'
ALLOWED_HOSTS = config['allowedHosts']
