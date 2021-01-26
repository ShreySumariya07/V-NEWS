# Generated by Django 3.0.8 on 2021-01-20 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Saved_News',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('abtsract', models.CharField(max_length=500)),
                ('web_url', models.URLField()),
                ('image_url', models.URLField()),
                ('title', models.CharField(max_length=300)),
                ('published_date', models.DateField()),
            ],
        ),
    ]
