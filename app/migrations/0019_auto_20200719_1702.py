# Generated by Django 3.0.3 on 2020-07-19 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20200719_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskgroup',
            name='task_id',
            field=models.ManyToManyField(to='app.Task'),
        ),
        migrations.DeleteModel(
            name='GroupIDTask',
        ),
    ]