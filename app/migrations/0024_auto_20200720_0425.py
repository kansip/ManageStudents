# Generated by Django 3.0.3 on 2020-07-20 01:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_auto_20200720_0304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskanswers',
            old_name='author',
            new_name='user',
        ),
    ]
