
import dj_database_url
import os
from pathlib import Path
from bleach.css_sanitizer import CSSSanitizer


BASE_DIR = Path(__file__).resolve().parent.parent

#Nunca dejes la clave secreta expuesta en producción
# Usa variables de entorno en Render:
# En Render, la defines en el panel de Environment → SECRET_KEY
SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-de-desarrollo')

#Desactiva el modo debug en producción
DEBUG = os.environ.get('DEBUG', 'False') == 'True'



# Render agregará automáticamente tu dominio, pero puedes añadir otros si quieres
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Apps
INSTALLED_APPS = [

     # my apps
    'blog',
    'accounts',
    'friends',
    'collaborators',
    'notifications',
    'emails',
   
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

     # Third party apps
    'django_bootstrap5',
    'cloudinary', 
    'cloudinary_storage',
    'tinymce',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Para servir archivos estáticos correctamente en producción
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'www.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.context_processors.unread_notifications_counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'www.wsgi.application'


# Base de datos (Render usará una variable DATABASE_URL si la defines)

if os.environ.get('RENDER'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,  
        )
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Custom User model
AUTH_USER_MODEL = 'accounts.NewUser' 

# Configuración regional
LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


#Archivos estáticos y media
STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Redirecciones de login/logout
LOGIN_REDIRECT_URL = 'blog:blogs_list'
LOGOUT_REDIRECT_URL = 'blog:home'
LOGIN_URL = 'accounts:login'

#Archivos media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

#Email backend settings

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

TINYMCE_DEFAULT_CONFIG = {
    "height": 400,
    "width": "100%",
    "menubar": False,
    "plugins": (
        "advlist autolink lists link image charmap preview anchor "
        "searchreplace visualblocks code fullscreen "
        "insertdatetime media table help wordcount"
    ),
    "toolbar": (
        "undo redo | formatselect | "
        "bold italic underline | forecolor backcolor fontsize | "
        "alignleft aligncenter alignright alignjustify | "
        "bullist numlist outdent indent | "
        "link image | code | help"
    ),
    "branding": False,
    "image_uploadtab": True,
}


BLEACH_ALLOWED_TAGS = [
    "p", "br",
    "strong", "b", "em", "i", "u",
    "ul", "ol", "li",
    "a", "img", "span",
]

BLEACH_ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "target", "rel"],
    "img": ["src", "alt", "width", "height"],
    "span": ["style"],
    "p": ["style"],
}

BLEACH_ALLOWED_PROTOCOLS = ["http", "https"]

BLEACH_CSS_SANITIZER = CSSSanitizer(
    allowed_css_properties=[
        "color",
        "background-color",
        "font-size",
        "text-align",
    ]
)



#default storage
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}




