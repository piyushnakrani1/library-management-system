from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid
from django.core.exceptions import ValidationError
import re

class UserManager(BaseUserManager):
    """ Custom user manager where email is the unique identifier """

    def create_user(self, email, password=None):
        if not email:
            raise ValueError(_("Users must have an email address"))
        
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """ Create and return a superuser """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """ Custom User model without username, using email as the primary identifier """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30,blank=True, null=True)
    last_name = models.CharField(max_length=30,blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

def validate_isbn(value):
    """Validates ISBN-10 and ISBN-13 formats using regex and checksum rules."""
    isbn = value.replace("-", "").replace(" ", "")  # Remove hyphens and spaces

    # Validate ISBN-10
    if len(isbn) == 10 and re.match(r"^\d{9}[\dX]$", isbn):
        return validate_isbn_10(isbn)

    # Validate ISBN-13
    elif len(isbn) == 13 and isbn.isdigit():
        return validate_isbn_13(isbn)

    raise ValidationError("Invalid ISBN format. Use ISBN-10 or ISBN-13.")

def validate_isbn_10(isbn):
    """Validate ISBN-10 checksum."""
    total = sum((i + 1) * (10 if x == 'X' else int(x)) for i, x in enumerate(isbn))
    if total % 11 != 0:
        raise ValidationError("Invalid ISBN-10 checksum.")

def validate_isbn_13(isbn):
    """Validate ISBN-13 checksum."""
    total = sum((int(isbn[i]) * (1 if i % 2 == 0 else 3)) for i in range(12))
    check_digit = (10 - (total % 10)) % 10
    if check_digit != int(isbn[-1]):
        raise ValidationError("Invalid ISBN-13 checksum.")

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=17, unique=True, validators=[validate_isbn])
    page_count = models.IntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def is_active(self):
        return self.returned_at is None
