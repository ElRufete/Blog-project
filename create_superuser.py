
import os
import django

# Carga la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'www.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' creado correctamente.")
else:
    print(f"El superusuario '{username}' ya existe.")

