from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Manager class to manage user-model
class CustomUserManager(BaseUserManager):
    # Create regular users
    def create_user(self, email, company_name, first_name, last_name, gender, phone, password=None):
        # Check basic validations for the required fields of "CustomUser" class
        if not email:
            raise ValueError('Email is required!')
        
        #  Create a user model
        user = self.model(
            email=self.normalize_email(email),
            company_name=company_name,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Create superusers
    def create_superuser(self, email, company_name, first_name, last_name, gender, phone, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            company_name=company_name,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone=phone,
            password=password
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Custom Uesr Model
CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]
class CustomUser(AbstractBaseUser):
    # User Info
    email = models.EmailField(verbose_name='Email', max_length=60, unique=True)
    company_name = models.CharField(verbose_name='Company Name', max_length=200, blank=True, default='Not Available')
    phone = models.CharField(verbose_name='Company Phone', max_length=20, blank=True, default='Null')
    # User Info [Extra]
    first_name = models.CharField(verbose_name='First Name', max_length=50, blank=True, default='Anonymous')
    last_name = models.CharField(verbose_name='Last Name', max_length=50, blank=True, default='User')
    gender = models.CharField(verbose_name='Gender', max_length=10, choices=CHOICES, default='Male')
    # Registration
    date_joined = models.DateField(verbose_name='Date Joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last Login', auto_now_add=True)
    # Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "User List"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company_name', 'phone', 'first_name', 'last_name', 'gender']

    # Define the base user model manager
    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.company_name

    def get_full_name(self):
        # The user is identified by their email address
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
