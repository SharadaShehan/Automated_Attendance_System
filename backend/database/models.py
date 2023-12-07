from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Role(models.Model):
    name = models.CharField(max_length=30, unique=False, null=False, blank=False)
    is_manager = models.BooleanField(default=False)
    is_executive = models.BooleanField(default=False)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, editable=False, null=False, blank=False)
    default_key = models.BigIntegerField(default=0, editable=False, null=True, blank=True, unique=False)

class Company(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    style_guide = models.JSONField(null=True, blank=True)
    company_api_code = models.BigIntegerField(unique=True, editable=False, null=True, blank=True)
    default_role_key = models.BigIntegerField(unique=True, editable=False, null=True, blank=True)
    default_executive_id = models.IntegerField(null=True, blank=True, default=0)
    default_executive_api_code = models.BigIntegerField(null=True, blank=True, default=0)

class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, company=None, role=None, user_api_code=None, first_name="", last_name="", picture=None, attendance=None, email_notifications=False, *args, **kwargs):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not company:
            raise ValueError("User must have a company")
        if not role:
            raise ValueError("User must have a role")
        if not user_api_code:
            raise ValueError("User must have a user_api_code")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)  # change password to hash
        user.company = company
        user.role = role
        user.user_api_code = user_api_code
        user.first_name = first_name
        user.last_name = last_name
        user.picture =picture
        user.attendance = attendance
        user.email_notifications = email_notifications
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, company=None, role=None, user_api_code=None, first_name="", last_name="", picture=None, attendance=None, email_notifications=False, *args, **kwargs):
        # role is an integer argument in this case
        user = self.create_user(
            email,
            password=password,
            company=Company.objects.get(pk=company),
            role=Role.objects.get(pk=role),
            user_api_code = user_api_code,
            first_name=first_name,
            last_name=last_name,
            picture=picture,
            attendance=attendance,
            email_notifications=email_notifications
        )
        return user

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    user_api_code = models.BigIntegerField(unique=True, editable=False, null=True, blank=True)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    picture = models.ImageField(upload_to='pictures/', null=True, blank=True)
    attendance = models.JSONField(null=True, blank=True)
    email_notifications = models.BooleanField(default=False)

    username = models.CharField(max_length=50, unique=False, default="")
    is_staff = models.BooleanField(default=False, editable=False)
    is_superuser = models.BooleanField(default=False, editable=False)
    is_active = models.BooleanField(default=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company', 'first_name', 'last_name', 'picture']    # This specifies which fields are required along with USERNAME_FIELD and password for user registration

    objects = UserManager()




