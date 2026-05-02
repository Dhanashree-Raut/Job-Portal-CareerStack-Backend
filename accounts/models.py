from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.contrib.auth.models import Group


class User(AbstractUser):
    """
    Custom User model that extends Django's default User.
    We add a 'role' field to distinguish between
    job seekers, employers, and admins.
    """

    class Role(models.TextChoices):
        JOB_SEEKER = 'job_seeker', 'Job Seeker'
        EMPLOYER = 'employer', 'Employer'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.JOB_SEEKER
    )

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    # Job Seeker specific fields
    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )
    skills = models.TextField(blank=True, null=True)

    # Employer specific fields
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)

    # ✅ FIX — override groups and user_permissions with unique related_name
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # changed from default 'user_set'
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # changed from default 'user_set'
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.role})"

    @property
    def is_job_seeker(self):
        return self.role == self.Role.JOB_SEEKER

    @property
    def is_employer(self):
        return self.role == self.Role.EMPLOYER

    @property
    def is_admin_user(self):
        return self.role == self.Role.ADMIN