from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Role(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False, blank=False)
    has_read_permission = models.BooleanField(default=False)
    has_edit_permission = models.BooleanField(default=False)


class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, role=None, first_name="", last_name="", gender=None,
                    encodings=None, picture=None, attendance=None, notifications=False, *args, **kwargs):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not role:
            raise ValueError("User must have a role")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        if not gender:
            raise ValueError("User must have a gender")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)  # change password to hash
        user.role = role
        user.first_name = first_name
        user.last_name = last_name
        user.gender = gender
        user.encodings = encodings
        user.picture = picture
        user.attendance = attendance
        user.notifications = notifications
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, role=None, first_name="", last_name="", gender=None,
                         encodings=None, picture=None, attendance=None, notifications=False, *args, **kwargs):
        # role is an integer argument in this case
        user = self.create_user(
            email,
            password=password,
            role=Role.objects.get(pk=role),
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            encodings=encodings,
            picture=picture,
            attendance=attendance,
            notifications=notifications
        )
        return user


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    gender = models.CharField(max_length=10, null=False, blank=False)
    picture = models.ImageField(upload_to='pictures/', null=True, blank=True)
    attendance = models.JSONField(null=True, blank=True)
    notifications = models.BooleanField(default=True)
    encodings = models.JSONField(null=True, blank=True)

    username = models.CharField(max_length=50, unique=False, default="")
    is_staff = models.BooleanField(default=False, editable=False)
    is_superuser = models.BooleanField(default=False, editable=False)
    is_active = models.BooleanField(default=True, editable=False)

    USERNAME_FIELD = 'email'
    # This specifies which fields are required along with USERNAME_FIELD and password for user registration
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender']

    objects = UserManager()


class CompanyInstanceManager(models.Manager):
    def get_company(self):
        instance, created = self.get_or_create(pk=1)
        return instance


class Company(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False, blank=False)
    default_role = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, blank=False)
    username = models.CharField(max_length=50, null=False, blank=False, default="admin")
    password = models.CharField(max_length=162, null=False, blank=False, default="password")
    init_token = models.CharField(max_length=64, null=False, blank=False, default="init_token")
    access_token = models.CharField(max_length=64, null=False, blank=False, default="access_token")

    objects = CompanyInstanceManager()

    def save(self, *args, **kwargs):
        if not self.pk and Company.objects.exists():
            raise Exception("Only one company can be created")
        self.pk = 1
        return super(Company, self).save(*args, **kwargs)
