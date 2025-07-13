from django.db import models

# Create your models here.
# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any additional fields you want for a user profile
    # For example:
    # first_name = models.CharField(max_length=100, blank=True) # Or use User.first_name
    # last_name = models.CharField(max_length=100, blank=True)  # Or use User.last_name
    bio = models.TextField(max_length=500, blank=True)
    address_line_1 = models.CharField(max_length=255, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    state_province_region = models.CharField(max_length=100, blank=True) # Or state/province
    postal_zip_code = models.CharField(max_length=20, blank=True) # Or zip_code
    country = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    # profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    profile_picture_url = models.URLField(max_length=500, blank=True, null=True, help_text="Enter a URL to an image for your profile picture.")
    

    def __str__(self):
        return f'{self.user.username} Profile'

# Signal to create or update the user profile automatically whenever a User instance is saved.
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()