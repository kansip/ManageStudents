# Generated by Django 3.0.3 on 2020-08-10 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20200810_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentgroup',
            name='name',
            field=models.CharField(default=32, max_length=10),
            preserve_default=False,
        ),
    ]
