# Generated by Django 5.0.7 on 2024-07-18 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_app', '0005_userprofile_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='d_profile.jfif', null=True, upload_to=''),
        ),
    ]
