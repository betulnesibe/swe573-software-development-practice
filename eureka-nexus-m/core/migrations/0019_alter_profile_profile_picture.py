# Generated by Django 5.1.3 on 2024-12-16 04:45

import core.models.base_models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_userfollower'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=core.models.base_models.get_unique_profile_path),
        ),
    ]
