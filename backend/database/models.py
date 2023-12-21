from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Role(models.Model):
    name = models.CharField(max_length=30, unique=False, null=False, blank=False)
    is_manager = models.BooleanField(default=False)
    is_executive = models.BooleanField(default=False)
    default_key = models.BigIntegerField(default=0, editable=False, null=True, blank=True, unique=False)

class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, role=None, first_name="", last_name="", picture=None,
                    attendance=None, notifications=False, *args, **kwargs):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not role:
            raise ValueError("User must have a role")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)  # change password to hash
        user.role = role
        user.first_name = first_name
        user.last_name = last_name
        user.picture = picture
        user.attendance = attendance
        user.notifications = notifications
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, role=None, first_name="", last_name="", picture=None,
                         attendance=None, notifications=False, *args, **kwargs):
        # role is an integer argument in this case
        user = self.create_user(
            email,
            password=password,
            role=Role.objects.get(pk=role),
            first_name=first_name,
            last_name=last_name,
            picture=picture,
            attendance=attendance,
            notifications=notifications
        )
        return user

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    picture = models.ImageField(upload_to='pictures/', null=True, blank=True)
    attendance = models.JSONField(null=True, blank=True)
    notifications = models.BooleanField(default=True)

    username = models.CharField(max_length=50, unique=False, default="")
    is_staff = models.BooleanField(default=False, editable=False)
    is_superuser = models.BooleanField(default=False, editable=False)
    is_active = models.BooleanField(default=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'picture']    # This specifies which fields are required along with USERNAME_FIELD and password for user registration

    objects = UserManager()




