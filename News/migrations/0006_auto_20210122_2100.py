# Generated by Django 3.0.8 on 2021-01-22 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0005_auto_20210121_1944'),
    ]

    operations = [
        migrations.RenameField(
            model_name='savednews',
            old_name='abtsract',
            new_name='abstract',
        ),
    ]
