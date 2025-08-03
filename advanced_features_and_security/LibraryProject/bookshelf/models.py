from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    class Meta:
        """
        Meta class defining custom permissions for the Book model to control
        actions such as viewing, creating, editing, or deleting instances.
        """
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]

    def __str__(self):
        return self.title


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for CustomUser model that handles user creation
    and queries, ensuring it can manage the added fields effectively.
    """

    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a regular user with the given username, email, and password.
        Handles the new fields correctly.
        """
        if not username:
            raise ValueError(_('The Username field must be set'))

        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a superuser with the given username, email, and password.
        Ensures administrative users can still be created with the required fields.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model that extends AbstractUser with additional fields
    and functionality for the application's specific needs.
    """

    # Additional fields beyond Django's built-in user model
    date_of_birth = models.DateField(
        _('Date of Birth'),
        null=True,
        blank=True,
        help_text=_('Enter your date of birth')
    )

    profile_photo = models.ImageField(
        _('Profile Photo'),
        upload_to='profile_photos/',
        null=True,
        blank=True,
        help_text=_('Upload a profile photo')
    )

    # Use the custom user manager
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.first_name

    @property
    def age(self):
        """
        Calculate and return the user's age based on date_of_birth.
        """
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
