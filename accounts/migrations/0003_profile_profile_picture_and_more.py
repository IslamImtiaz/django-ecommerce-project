# Generated by Django 5.1.5 on 2025-06-22 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_profile_picture_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, help_text='Upload a profile picture.', null=True, upload_to='profile_pics/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture_url',
            field=models.URLField(blank=True, help_text='Or, enter a URL to an image for your profile picture.', max_length=500, null=True),
        ),
    ]
