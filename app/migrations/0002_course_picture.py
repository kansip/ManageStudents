# Generated by Django 2.2 on 2020-05-20 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='picture',
            field=models.ImageField(blank=True, upload_to='photos'),
        ),
    ]
