import os
DEBUG = True
STATIC_S3 = False
# for k in os.environ:
#     print(k, os.environ[k])

# Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTING_DIR = os.path.join(BASE_DIR, 'fastcampus')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')


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
if 'RDS_HOSTNAME' in os.environ or 'EB_IS_COMMAND_LEADER' in os.environ or 'AWS_ELB_HOME' in os.environ or STATIC_S3:
    AWS_HEADERS = {
        'Expires': 'Thu, 31 Dec 2199 20:00:00 GMT',
        'Cache-Control': 'max-age=94608000',
    }
    AWS_STORAGE_BUCKET_NAME = 'fastcampus-s3'
    AWS_ACCESS_KEY_ID = 'AKIAIJ6L2YNR3H3VQYYQ'
    AWS_SECRET_ACCESS_KEY = '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'
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

    STATICFILES_LOCATION = 'static'
    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
    STATICFILES_STORAGE = 'fastcampus.custom_storages.StaticStorage'

    MEDIAFILES_LOCATION = 'media'
    MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
    DEFAULT_FILE_STORAGE = 'fastcampus.custom_storages.MediaStorage'

    COMPRESS_LOCATION = 'compress'
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
if 'RDS_HOSTNAME' in os.environ or 'EB_IS_COMMAND_LEADER' in os.environ or 'AWS_ELB_HOME' in os.environ :
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'fastcampus',
            'USER': 'lhy',
            'PASSWORD': 'gksdud!027',
            'HOST': 'fastcampus.cryfbwalveyh.ap-northeast-2.rds.amazonaws.com',
            'PORT': '5432',
            # 'NAME': os.environ['RDS_DB_NAME'],
            # 'USER': os.environ['RDS_USERNAME'],
            # 'PASSWORD': os.environ['RDS_PASSWORD'],
            # 'HOST': os.environ['RDS_HOSTNAME'],
            # 'PORT': os.environ['RDS_PORT'],
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'fastcampus',
            'USER': '',
            'PASSWORD': '',
            'HOST': 'localhost',
            'POST': '5432',
            'OPTIONS': {
                # 'read_default_file': os.path.join(SETTING_DIR, 'db_local.cnf'),
            },
        },
    }



# Other settings
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

ROOT_URLCONF = 'fastcampus.urls'
WSGI_APPLICATION = 'fastcampus.wsgi.application'
SECRET_KEY = 'u*8!!mqh10rzxgdom1&1y%x1d&-8!$sd*#_lr9&n5mp5+nh_jy'
ALLOWED_HOSTS = []
