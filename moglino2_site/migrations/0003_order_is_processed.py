# Generated by Django 4.2.7 on 2023-11-18 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moglino2_site', '0002_alter_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_processed',
            field=models.BooleanField(default=False),
        ),
    ]
