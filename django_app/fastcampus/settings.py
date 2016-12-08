import urllib.parse
import json
import sys
import os

# Debug check
# DEBUG = True
# if 'RDS_HOSTNAME' in os.environ or 'EB_IS_COMMAND_LEADER' in os.environ or 'AWS_ELB_HOME' in os.environ:
#     DEBUG = False
# for item in os.environ:
#     print(item, os.environ[item])


DEBUG = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')
if 'USER' in os.environ and os.environ['USER'] == 'Arcanelux':
    DEBUG = True
print('DEBUG : %s' % DEBUG)

# USING_AWS = False
USING_AWS = True
if os.environ.get('aws', False):
    USING_AWS = True
print('USING_AWS : %s' % USING_AWS)

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
# COMPRESS_ROOT = STATIC_ROOT
COMPRESS_PRECOMPILERS = (
    ('text/sass', 'sass {infile} {outfile}'),
)
COMPRESS_CACHEABLE_PRECOMPILERS = (
    'text/sass',
)
COMPRESS_ENABLED = True

# Celery
# BROKER_URL = 'amqp://guest:guest@localhost//'

# AWS
if not DEBUG or USING_AWS:
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

    COMPRESS_LOCATION = 'compress'
    COMPRESS_URL = STATIC_URL
    COMPRESS_STORAGE = STATICFILES_STORAGE
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

# Celery with SQS
if not DEBUG or USING_AWS:
    AWS_ACCESS_KEY_ID = config['aws']['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = config['aws']['AWS_SECRET_ACCESS_KEY']
    CELERY_BROKER_URL = 'sqs://{}:{}@'.format(
        urllib.parse.quote(AWS_ACCESS_KEY_ID, safe=''),
        urllib.parse.quote(AWS_SECRET_ACCESS_KEY, safe=''),
    )
    CELERY_BROKER_TRANSPORT_OPTIONS = {
        'region': 'us-east-1',
        'polling_interval': 3,
        'visibility_timeout': 3600,
        'queue_name_prefix': 'lhy-',
    }
else:
    pass

# Celery
CELERY_RESULT_BACKEND = 'django-db'
CELERY_IMPORTS = (
    'apis.mail.asdf',
)
print(CELERY_BROKER_URL)

# Auth
AUTH_USER_MODEL = 'member_rest_auth.MyUser'
SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL
AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
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
# LOGIN_URL = 'member:login'

# python-social-auth
SOCIAL_AUTH_FACEBOOK_KEY = config['facebook']['FACEBOOK_APP_ID']
SOCIAL_AUTH_FACEBOOK_SECRET = config['facebook']['FACEBOOK_SECRET_CODE']
SOCIAL_AUTH_PIPELINE = (
    # 사용자에 대한 정보를 얻고 간단한 형식으로 반환하여 나중에 사용자 인스턴스를 만듭니다.
    # 경우에 따라 세부 정보가 이미 공급자의 인증 응답에 포함되어 있지만 때로는 공급자 API에 충돌 할 수 있습니다.
    'social.pipeline.social_auth.social_details',

    # 우리가 제공하는 서비스에서 Social uid를 받으십시오.
    # uid는 공급자로부터 주어진 사용자의 고유한 식별자입니다.
    'social.pipeline.social_auth.social_uid',

    # 현재 인증 프로세스가 현재 프로젝트에서 유효하다는 것을 확인합니다.
    # 이는 허용 목록 (정의 된 경우)이 적용되는 이메일 및 도메인입니다.
    'social.pipeline.social_auth.auth_allowed',

    # 현재 소셜 계정이 이미 사이트에 연결되어 있는지 확인합니다.
    'social.pipeline.social_auth.social_user',

    # 이 사람의 사용자 이름을 확인하고, 충돌이 있으면 끝에 임의의 문자열을 추가합니다.
    'social.pipeline.user.get_username',

    # 사용자에게 전자 메일 주소를 확인하는 유효성 검사 전자 메일을 보냅니다.
    # 기본적으로 사용하지 않도록 설정되어 있습니다.
    # 'social.pipeline.mail.mail_validation',

    # 현재 소셜 세부 정보를 유사한 이메일 주소를 가진 다른 사용자 계정과 연결합니다.
    # 기본적으로 사용하지 않도록 설정되어 있습니다.
    # 'social.pipeline.social_auth.associate_by_email',

    # 아직 계정을 찾지 못한 경우 사용자 계정을 만듭니다.
    'social.pipeline.user.create_user',

    # 이 사용자와 소셜 계정을 연결 한 레코드를 만듭니다.
    'social.pipeline.social_auth.associate_user',

    # 소셜 레코드의 extra_data 필드에 설정에 지정된 값
    # (기본값은 access_token 등)을 채웁니다.
    'social.pipeline.social_auth.load_extra_data',

    # 인증 서비스에서 변경된 정보로 사용자 레코드를 업데이트합니다.
    'social.pipeline.user.user_details',
)

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

    'rest_framework',
    'rest_framework.authtoken',
    'social.apps.django_app.default',
    'rest_social_auth',

    'storages',
    'compressor',
    'markdownx',
    'adminsortable',
    'django_celery_results',
    'django_celery_beat',
    'corsheaders',

    'apis',
    'course',
    'member',
    'member_rest_auth',
    'projects.blog',
    'projects.photo',
    'projects.video',
    'projects.sns',
]

CORS_ORIGIN_WHITELIST = (
    'localhost:4000',
)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
}

# django-markdownx
# Markdownify
MARKDOWNX_MARKDOWNIFY_FUNCTION = 'markdownx.utils.markdownify' # Default function that compiles markdown using defined extensions. Using custom function can allow you to pre-process or post-process markdown text. See below for more info.

# Markdown extensions
MARKDOWNX_MARKDOWN_EXTENSIONS = [] # List of used markdown extensions. See below for more info.
MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS = {} # Configuration object for used markdown extensions

# Markdown urls
MARKDOWNX_URLS_PATH = '/markdownx/markdownify/' # URL that returns compiled markdown text.
MARKDOWNX_UPLOAD_URLS_PATH = '/markdownx/upload/' # URL that accepts file uploads, returns markdown notation of the image.

# Media path
MARKDOWNX_MEDIA_PATH = 'markdownx/' # Path, where images will be stored in MEDIA_ROOT folder

# Image
MARKDOWNX_UPLOAD_MAX_SIZE = 52428800 # 50MB - maximum file size
MARKDOWNX_UPLOAD_CONTENT_TYPES = ['image/jpeg', 'image/png'] # Acceptable file content types
MARKDOWNX_IMAGE_MAX_SIZE = {'size': (500, 500), 'quality': 90,} # Different options describing final image processing: size, compression etc. See below for more info.

# Editor
MARKDOWNX_EDITOR_RESIZABLE = True # Update editor's height to inner content height while typing


# Django Admin Sortable


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
