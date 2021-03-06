"""
Django settings for timpass project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# DEBUG = bool(os.environ.get('DEBUG', False))

if DEBUG:
    from development_settings import *
else:
    from production_settings import *

ROOT_URLCONF = 'pichrr.urls'

WSGI_APPLICATION = 'pichrr.wsgi.application'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'social.apps.django_app.default',
    'oauth2_provider',
    'rest_framework_social_oauth2',
    'debug_toolbar',
    'user_profile',
    'post',
    'tags',
    'django_comments',
    'djcelery',
    'dbbackup',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.tz',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ),
}

SITE_ID = 1

POSTS_PER_PAGE = 9

#Celery_generic settings

# Task result life time until they will be deleted
CELERY_TASK_RESULT_EXPIRES = 7 * 86400 # 7 days

# Needed for worker monitoring
CELERY_SEND_EVENTS = True
# Where to store periodic tasks (needed for scheduler)
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_AVATAR_IMAGE = 'img/avatar/avatar.jpg'
# AVATAR_URL_PREFIX = '/media/img/avatar/'
AVATAR_ROOT = os.path.join(MEDIA_ROOT, 'avatar')
AUTH_PROFILE_MODULE = 'user_profile.UserProfile'
MAX_PHOTO_SIZE = 2000
PHOTO_URL_PREFIX = '/media/'
PHOTO_ROOT = MEDIA_ROOT


COMMENT_MAX_LENGTH = 500

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email, age_range'
}

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is were emails and domains whitelists are applied (if
    # defined).
    'social.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social.pipeline.social_auth.social_user',

    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    'social.pipeline.user.get_username',

    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social.pipeline.mail.mail_validation',

    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    'social.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social.pipeline.user.create_user',

    # Create the record that associated the social account with this user.
    'social.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'social.pipeline.user.user_details'
)

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'


ACCOUNT_ADAPTER ="allauth.account.adapter.DefaultAccountAdapter"
    # Specifies the adapter class to use, allowing you to alter certain default behaviour.
ACCOUNT_AUTHENTICATION_METHOD ="username_email"
    # Specifies the login method to use - whether the user logs in by entering their username, e-mail address, or either one of both. Setting this to email requires ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_CONFIRM_EMAIL_ON_GET =False
    # Determines whether or not an e-mail address is automatically confirmed by a mere GET request.
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL
    # The URL to redirect to after a successful e-mail confirmation, in case no user is logged in.
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL =None
    # The URL to redirect to after a successful e-mail confirmation, in case of an authenticated user. Set to None to use settings.LOGIN_REDIRECT_URL.
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =3
    # Determines the expiration date of email confirmation mails (# of days).
ACCOUNT_EMAIL_REQUIRED =True
    # The user is required to hand over an e-mail address when signing up.
ACCOUNT_EMAIL_VERIFICATION ="mandatory"
    # Determines the e-mail verification method during signup - choose one of "mandatory", "optional", or "none". When set to "mandatory"
    #  the user is blocked from logging in until the email address is verified. Choose "optional" or "none" to allow logins with an
    # unverified e-mail address. In case of "optional", the e-mail verification mail is still sent, whereas in case of "none" no e-mail verification mails are sent.
ACCOUNT_EMAIL_SUBJECT_PREFIX ="tambasha "
    # Subject-line prefix to use for email messages sent. By default, the name of the current Site (django.contrib.sites) is used.
ACCOUNT_DEFAULT_HTTP_PROTOCOL ="http"
    # The default protocol used for when generating URLs, e.g. for the password forgotten procedure. Note that this is a default only - see the section on HTTPS for more information.
ACCOUNT_FORMS ={}
    # Used to override forms, for example: {'login': 'myapp.forms.LoginForm'}
ACCOUNT_LOGOUT_ON_GET =True
    # Determines whether or not the user is automatically logged out by a mere GET request. See documentation for the LogoutView for details.
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE =True
    # Determines whether or not the user is automatically logged out after changing the password. See documentation for Django's session invalidation on password change. (Django 1.7+)
ACCOUNT_LOGOUT_REDIRECT_URL ="/"
    # The URL (or URL name) to return to after the user logs out. This is the counterpart to Django's LOGIN_REDIRECT_URL.
ACCOUNT_SIGNUP_FORM_CLASS =None
    # A string pointing to a custom form class (e.g. 'myapp.forms.SignupForm') that is used during signup to ask the user for additional
    # input (e.g. newsletter signup, birth date). This class should implement a def signup(self, request, user) method, where user represents the newly signed up user.
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION =True
    # When signing up, let the user type in their password twice to avoid typo's.
ACCOUNT_UNIQUE_EMAIL =True
    # Enforce uniqueness of e-mail addresses.
ACCOUNT_USER_MODEL_USERNAME_FIELD ="username"
    # The name of the field containing the username, if any. See custom user models.
ACCOUNT_USER_MODEL_EMAIL_FIELD ="email"
    # The name of the field containing the email, if any. See custom user models.
# ACCOUNT_USER_DISPLAY =a callable returning user.username
    # A callable (or string of the form 'some.module.callable_name') that takes a user as its only argument and returns the display name of the user.
    #  The default implementation returns user.username.
ACCOUNT_USERNAME_MIN_LENGTH =3
    # An integer specifying the minimum allowed length of a username.
ACCOUNT_USERNAME_BLACKLIST =['admin', 'settings', 'news', 'about', 'help', 'signin', 'signup',
        'signout', 'terms', 'privacy', 'cookie', 'new', 'login', 'logout', 'administrator',
        'join', 'account', 'username', 'root', 'blog', 'user', 'users', 'billing', 'subscribe',
        'reviews', 'review', 'blog', 'blogs', 'edit', 'mail', 'email', 'home', 'job', 'jobs',
        'contribute', 'newsletter', 'shop', 'profile', 'register', 'auth', 'authentication',
        'campaign', 'config', 'delete', 'remove', 'forum', 'forums', 'download', 'downloads',
        'contact', 'blogs', 'feed', 'faq', 'intranet', 'log', 'registration', 'search',
        'explore', 'rss', 'support', 'status', 'static', 'media', 'setting', 'css', 'js',
        'follow', 'activity']
    # A list of usernames that can't be used by user.
ACCOUNT_USERNAME_REQUIRED =True
    # The user is required to enter a username when signing up. Note that the user will be asked to do so even if ACCOUNT_AUTHENTICATION_METHOD is set to email.
    #  Set to False when you do not wish to prompt the user to enter a username.
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE =False
    # render_value parameter as passed to PasswordInput fields.
ACCOUNT_PASSWORD_MIN_LENGTH =6
    # An integer specifying the minimum password length.
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION =False
    # The default behaviour is not log users in and to redirect them to ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL.
    # By changing this setting to True, users will automatically be logged in once they confirm their email address.
    #  Note however that this only works when confirming the email address immediately after signing up, assuming users didn't close their browser
    # or used some sort of private browsing mode.
ACCOUNT_LOGIN_ON_PASSWORD_RESET =False
    # By changing this setting to True, users will automatically be logged in once they have reset their password.
    #  By default they are redirected to the password reset done page.
ACCOUNT_SESSION_REMEMBER =None
    # Controls the life time of the session. Set to None to ask the user ("Remember me?"), False to not remember, and True to always remember.
ACCOUNT_SESSION_COOKIE_AGE =1814400
    # How long before the session cookie expires in seconds. Defaults to 1814400 seconds, or 3 weeks.



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'production_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/main.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_false'],
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/main_debug.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_true'],
        },
        'null': {
            "class": 'django.utils.log.NullHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['null', ],
        },
        'py.warnings': {
            'handlers': ['null', ],
        },
        '': {
            'handlers': ['console', 'production_file', 'debug_file'],
            'level': "DEBUG",
        },
    }
}
