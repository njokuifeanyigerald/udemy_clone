from django.db import models
from helpers.models import TrackingModel
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

# FOR THE TOKEN PART (JWT)
# from django.conf import settings
# from rest_framework_simplejwt.tokens import RefreshToken


class MyUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        if not name:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        name = self.model.normalize_username(name)
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, name, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(name, email, password, **extra_fields)


    def create_superuser(self, name, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(name, email, password, **extra_fields)


class User(TrackingModel, AbstractBaseUser, PermissionsMixin):

    name = models.CharField(
        _("name"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        )
        
    )
    email = models.EmailField(
        _("email address"),
        blank=False,
        unique=True,
        help_text=_("Email is required"),
        error_messages={
                "unique": _("A user with email already exists."),
            },)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    email_verified = models.BooleanField(
        _("email_verified"),
        default=False,
        help_text=_(
            "Designates whether this user email is verified "
        ),
    )
    paid_courses = models.ManyToManyField("courses.Course", related_name="courses")

   

    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]


    def __str__(self):
        return f'Name: {self.name} and Email: { self.email}'

    def get_all_courses(self):
        courses = []
        # because it is a many to many field
        for course in self.paid_courses.all():
            courses.append(course.course_uuid)

        return courses 


   