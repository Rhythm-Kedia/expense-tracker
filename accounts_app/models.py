from django.contrib.auth.models import AbstractUser
from django.db import models
import os

def user_profile_image_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/profile_images/<filename>
    # MEDIA_ROOT is defined in settings.py
    return f'user_{instance.id}/profile_images/{filename}'

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to=user_profile_image_path, null=True, blank=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",  # Unique related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions_set",  # Unique related name
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return self.email

    def delete_profile_image(self):
        # Delete the profile image file when the user deletes their image
        if self.profile_image:
            if os.path.isfile(self.profile_image.path):
                os.remove(self.profile_image.path)
            self.profile_image = None
            self.save()