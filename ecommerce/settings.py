# """
# Django settings for ecommerce project.
# """

# import os
# from pathlib import Path
# from decouple import config
# import dj_database_url

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config('DEBUG', default='False', cast=bool)

# # Get allowed hosts from environment variable
# ALLOWED_HOSTS_STR = config('ALLOWED_HOSTS', default='')
# if ALLOWED_HOSTS_STR:
#     ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STR.split(',') if host.strip()]
# else:
#     # Default for local development
#     ALLOWED_HOSTS = ['localhost', '127.0.0.1'] if DEBUG else []


# # Application definition
# DJANGO_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'django.contrib.sites',
# ]

# THIRD_PARTY_APPS = [
#     'rest_framework',
#     'corsheaders',
#     'allauth',
#     'allauth.account',
#     'allauth.socialaccount',
#     'allauth.socialaccount.providers.google',
#     'allauth.socialaccount.providers.facebook',
#     'crispy_forms',
#     'crispy_bootstrap5',
#     'import_export',
#     'django_cleanup.apps.CleanupConfig',
#     'compressor',
#     "storages"
# ]

# LOCAL_APPS = [
#     'accounts',
#     'products',
#     'cart',
#     'orders',
#     'payments',
#     'reviews',
#     'wishlist',
#     'coupons',
#     'analytics',
#     'core',
# ]

# INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'django_ratelimit.middleware.RatelimitMiddleware',
#     "allauth.account.middleware.AccountMiddleware",
# ]

# ROOT_URLCONF = 'ecommerce.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.template.context_processors.media',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#                 'core.context_processors.cart',
#                 'core.context_processors.categories',
#                 'core.context_processors.wishlist_product_ids',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'ecommerce.wsgi.application'

# # Database
# DATABASES = {
#     'default': dj_database_url.config(
#         default=config('DATABASE_URL', default='sqlite:///db.sqlite3')
#     )
# }

# # Password validation
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

# # Internationalization
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'Asia/Karachi'  # Pakistan timezone
# USE_I18N = True
# USE_TZ = True

# # AWS S3 Configuration
# USE_S3 = config('USE_S3', default='False') == 'True'

# if USE_S3:
#     # AWS S3 Settings
#     AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
#     AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
#     AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
#     AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
#     AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
#     AWS_S3_OBJECT_PARAMETERS = {
#         'CacheControl': 'max-age=86400',
#     }
#     AWS_DEFAULT_ACL = 'public-read'
#     AWS_S3_FILE_OVERWRITE = False
#     AWS_QUERYSTRING_AUTH = False
    
#     # Static files
#     AWS_STATIC_LOCATION = 'static'
#     STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#     STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STATIC_LOCATION}/'
    
#     # Media files
#     AWS_MEDIA_LOCATION = 'media'
#     DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#     MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_MEDIA_LOCATION}/'
    
#     # Static files directories (for collectstatic)
#     STATICFILES_DIRS = [
#         BASE_DIR / 'static',
#     ]
# else:
#     # Local static and media files
#     STATIC_URL = '/static/'
#     STATIC_ROOT = BASE_DIR / 'staticfiles'
#     STATICFILES_DIRS = [
#         BASE_DIR / 'static',
#     ]
    
#     MEDIA_URL = '/media/'
#     MEDIA_ROOT = BASE_DIR / 'media'

# STATICFILES_FINDERS = [
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#     'compressor.finders.CompressorFinder',
# ]

# # Default primary key field type
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # Custom User Model
# AUTH_USER_MODEL = 'accounts.User'

# # Authentication
# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',
#     'allauth.account.auth_backends.AuthenticationBackend',
# ]

# SITE_ID = 1

# # Allauth settings
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
# ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300

# # Allauth template settings
# ACCOUNT_TEMPLATE_EXTENSION = 'html'

# # Email settings
# EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
# EMAIL_HOST = config('EMAIL_HOST', default='')
# EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
# EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
# EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
# DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@ecommerce.com')

# # Crispy Forms
# CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
# CRISPY_TEMPLATE_PACK = "bootstrap5"

# # Cache settings
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#     }
# }
# # Session settings
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# SESSION_CACHE_ALIAS = 'default'
# SESSION_COOKIE_AGE = 86400  # 24 hours

# # Celery settings
# CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://127.0.0.1:6379/0')
# CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://127.0.0.1:6379/0')
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'

# # Stripe settings
# STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY', default='')
# STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')
# STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', default='')

# # PayPal settings
# PAYPAL_CLIENT_ID = config('PAYPAL_CLIENT_ID', default='')
# PAYPAL_CLIENT_SECRET = config('PAYPAL_CLIENT_SECRET', default='')
# PAYPAL_MODE = config('PAYPAL_MODE', default='sandbox')  # sandbox or live

# # Security settings
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = 'DENY'

# # HTTPS settings (only in production)
# if not DEBUG:
#     SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default='True', cast=bool)
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     SECURE_HSTS_SECONDS = 31536000
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#     SECURE_HSTS_PRELOAD = True
# else:
#     SECURE_SSL_REDIRECT = False
#     SESSION_COOKIE_SECURE = False
#     CSRF_COOKIE_SECURE = False
#     SECURE_HSTS_SECONDS = 0

# # CORS settings
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
#     'https://billowiest-aurelio-unconcreted.ngrok-free.dev'
# ]

# # Rate limiting
# RATELIMIT_USE_CACHE = 'default'

# # Logging
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': BASE_DIR / 'logs' / 'django.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     },
# }

# # Compressor settings
# COMPRESS_ENABLED = not DEBUG
# COMPRESS_CSS_FILTERS = [
#     'compressor.filters.css_default.CssAbsoluteFilter',
#     'compressor.filters.cssmin.rCSSMinFilter',
# ]
# COMPRESS_JS_FILTERS = [
#     'compressor.filters.jsmin.rJSMinFilter',
# ]

# if DEBUG:
#     INSTALLED_APPS += ['django_extensions', 'debug_toolbar']
#     MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
#     INTERNAL_IPS = ['127.0.0.1', 'localhost']

# # Try to import django_heroku (only available in production)
# try:
#     import django_heroku
# except ImportError:
#     django_heroku = None

# # Heroku specific settings
# if 'DYNO' in os.environ and django_heroku:
#     django_heroku.settings(locals(), staticfiles=False)  # We're using S3 for static files
    
#     # Ensure DATABASE_URL is used
#     DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

"""
Django settings for ecommerce project.
Optimized for Heroku deployment with AWS S3 media storage.
"""

import os
from pathlib import Path
from decouple import config
import dj_database_url

# -------------------------------------------------------------------
# BASE & SECRET
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="unsafe-secret-key")
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = [
    host.strip()
    for host in config("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")
    if host.strip()
]

# -------------------------------------------------------------------
# SITE INFO / PAYMENTS
# -------------------------------------------------------------------
SITE_BRAND_NAME = config("SITE_BRAND_NAME", default="LUNDKHWAR MOBILE CENTER")
EASYPAISA_NUMBER = config("EASYPAISA_NUMBER", default="03129151970")
JAZZCASH_NUMBER = config("JAZZCASH_NUMBER", default="03489278571")

# -------------------------------------------------------------------
# APPS
# -------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    "crispy_forms",
    "crispy_bootstrap5",
    "import_export",
    "django_cleanup.apps.CleanupConfig",
    "storages",
]

LOCAL_APPS = [
    "accounts",
    "products",
    "cart",
    "orders",
    "reviews",
    "wishlist",
    "coupons",
    "analytics",
    "core",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# -------------------------------------------------------------------
# MIDDLEWARE
# -------------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -------------------------------------------------------------------
# TEMPLATES
# -------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.cart",
                "core.context_processors.categories",
                "core.context_processors.wishlist_product_ids",
            ],
        },
    },
]

ROOT_URLCONF = "ecommerce.urls"
WSGI_APPLICATION = "ecommerce.wsgi.application"

# -------------------------------------------------------------------
# DATABASE
# -------------------------------------------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}

# -------------------------------------------------------------------
# PASSWORD VALIDATORS
# -------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# -------------------------------------------------------------------
# INTERNATIONALIZATION
# -------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Karachi"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# AUTH & ALLAUTH
# -------------------------------------------------------------------
AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300

SITE_ID = 1

# -------------------------------------------------------------------
# EMAIL
# -------------------------------------------------------------------
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@ecommerce.com")

# -------------------------------------------------------------------
# STATIC & MEDIA FILES (Heroku + S3)
# -------------------------------------------------------------------

USE_S3 = config("USE_S3", cast=bool, default=True)

if USE_S3:
    # ---------------------------
    # AWS S3 Settings
    # ---------------------------
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME", default="us-east-1")
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

    # ---------------------------
    # Static files (CSS, JS, images)
    # ---------------------------
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
    STATICFILES_STORAGE = "core.storage_backends.StaticStorage"
    STATICFILES_DIRS = [BASE_DIR / "static"]

    # ---------------------------
    # Media files (user uploads)
    # ---------------------------
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
    DEFAULT_FILE_STORAGE = "core.storage_backends.MediaStorage"

else:
    # ---------------------------
    # Local / WhiteNoise fallback
    # ---------------------------
    STATIC_URL = "/static/"
    STATIC_ROOT = BASE_DIR / "staticfiles"
    STATICFILES_DIRS = [BASE_DIR / "static"]
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

# Static files finders (without compressor)
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# -------------------------------------------------------------------
# SECURITY
# -------------------------------------------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# -------------------------------------------------------------------
# CORS
# -------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://yourfrontend.com",
]

# -------------------------------------------------------------------
# HEROKU
# -------------------------------------------------------------------
if "DYNO" in os.environ:
    import django_heroku

    django_heroku.settings(locals(), staticfiles=False)

# -------------------------------------------------------------------
# DEFAULT PRIMARY KEY
# -------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
