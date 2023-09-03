import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(
        self,
        username,
        first_name,
        last_name,
        email,
        contact_number,
        password=None,
        **extra_fields
    ):
        if not username:
            raise ValueError("The username must be set")

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            contact_number=contact_number,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def update_password(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set")

        user = self.get(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username,
        first_name,
        last_name,
        email,
        contact_number,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(
            username,
            first_name,
            last_name,
            email,
            contact_number,
            password,
            **extra_fields,
        )

    def create_staffuser(
        self,
        username,
        first_name,
        last_name,
        email,
        contact_number,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        return self.create_user(
            username,
            first_name,
            last_name,
            email,
            contact_number,
            password,
            **extra_fields,
        )


class Profile(AbstractUser):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]
    user_id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
    )
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default=None, null=True, blank=True
    )
    email = models.EmailField(max_length=255, unique=True)
    contact_number = models.BigIntegerField()
    password = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    # profile_image = models.ImageField(default='default_user.png', upload_to='/path')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "contact_number"]

    def __str__(self):
        return self.username

    def set_is_admin(self, value):
        self.is_admin = value
        self.save()

    @property
    def status_staff(self):
        return self.is_staff

    @property
    def status_admin(self):
        return self.is_admin
