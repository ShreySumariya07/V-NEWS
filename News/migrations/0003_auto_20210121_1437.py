# Generated by Django 3.0.8 on 2021-01-21 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0002_auto_20210120_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savednews',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
