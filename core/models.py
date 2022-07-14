from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

# Custom User Manager
class CustomUserManager(BaseUserManager) :
    def _create_user(self, email, password, first_name, last_name, mobile, **extra_fields) :
        if not email :
            raise ValueError("Email must be provided.")
        if not password :
            raise ValueError("Password is not provided.")
        
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            mobile = mobile,
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_user(self, email, password, first_name, last_name, mobile, **extra_fields) :
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, mobile, password, **extra_fields)
    

    def create_superuser(self, email, password, first_name, last_name, mobile, **extra_fields) :
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, first_name, last_name, mobile, **extra_fields)
        

# User Model
# Abstractbaseuser has password, last_login, is_active by default
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=50)
    address = models.CharField( max_length=250)

    # must needed, otherwise you won't be able to loginto django-admin.
    is_staff = models.BooleanField(default=True)
    
    # must needed, otherwise you won't be able to loginto django-admin.
    is_active = models.BooleanField(default=True)
    
    # this field we inherit from PermissionsMixin.
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','mobile']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'