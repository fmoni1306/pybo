from .base import *

ALLOWED_HOSTS = ['3.34.8.110']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []
DEBUG = False


# PostgreSQL 적용
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pybo',
        'USER': 'dbmasteruser',
        'PASSWORD': '6q}Z^TVHBG1_aqm`~OjeS+{h~oS7<1hW',
        'HOST': 'ls-31f7340c3549d2c2ab46f29bee6301ef8c0f67db.cx18kr6969b0.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

