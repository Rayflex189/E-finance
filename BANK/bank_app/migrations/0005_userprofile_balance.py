# Generated by Django 5.0.7 on 2024-07-18 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_app', '0004_alter_userprofile_account_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
