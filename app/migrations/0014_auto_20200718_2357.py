# Generated by Django 3.0.3 on 2020-07-18 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20200718_1802'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='data_open',
            new_name='data',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='open',
        ),
    ]