# Generated by Django 5.0.7 on 2024-07-18 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='Recipients_IBAN',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='Total_Transfer_Amount',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='current_date',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='estimated_delivery_time',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='image',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='mobile_number',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='recipent_bank',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='recipent_country',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='recipent_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='senders_bank',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='senders_country',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='senders_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='status_text',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='status_update',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='transaction',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_number',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='account_number',
            field=models.CharField(default='00000000000', max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
