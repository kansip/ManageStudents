# Generated by Django 3.0.3 on 2020-08-10 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='open',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='lesson',
            name='open',
            field=models.BooleanField(default=0),
        ),
    ]