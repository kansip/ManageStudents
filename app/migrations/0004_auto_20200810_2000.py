# Generated by Django 3.0.3 on 2020-08-10 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200810_1952'),
    ]

    operations = [
        migrations.RenameField(
            model_name='minisubject',
            old_name='subject_name',
            new_name='name',
        ),
    ]
