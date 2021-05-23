from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "t_company"

    def __str__(self):
        return 'Company "%s"' % self.name


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email address must be provided')

        if not password:
            raise ValueError('Password must be provided')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserAccountManager()

    email = models.EmailField(unique=True)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    company = models.ForeignKey(Company, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)

    class Meta:
        db_table = "t_user"

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email

    def __str__(self):
        return 'User "%s"' % self.email


class Skill(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "t_skill"

    def __str__(self):
        return 'Skill "%s"' % self.name
