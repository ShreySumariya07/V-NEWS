# Generated by Django 3.0.8 on 2021-01-23 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0007_savednews_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='savednews',
            old_name='user',
            new_name='us_id',
        ),
    ]
