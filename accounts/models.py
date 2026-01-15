from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from cloudinary.models import CloudinaryField
from cloudinary import CloudinaryImage


class CustomAccountManager(BaseUserManager):
    def create_user(self,email,user_name,password,**other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, 
                          **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,user_name,password,**other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Your staff status must be set to True'))
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Your superuser status must be set to True'))
        
        return self.create_user(email,user_name,password,**other_fields)


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    user_name = models.CharField(max_length= 20, unique=True)
    first_name = models.CharField(max_length= 100, blank = True)
    last_name = models.CharField(max_length= 140, blank= True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_("about"), max_length=500, blank=True)
    avatar = CloudinaryField('avatar', blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    
    def avatar_url(self, size=100):
        public_id = self.avatar.public_id if self.avatar else 'default_avatar_qmiibj'
        return CloudinaryImage(public_id).build_url(
            width=size,
            height=size, 
            crop='thumb', 
            gravity='face',
            radius="max",
            background='transparent',
            format='png',
            fetch_format='auto',
            quality='auto',
            )
    
    @property
    def avatar_small(self):
        return self.avatar_url(size=32)
    
    @property
    def avatar_medium(self):
        return self.avatar_url(size=50)
    
    @property
    def avatar_large(self):
        return self.avatar_url(size=128)
    
    def __str__(self):
        return self.user_name

