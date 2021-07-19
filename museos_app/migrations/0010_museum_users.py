# Generated by Django 3.2.4 on 2021-07-19 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos_app', '0009_remove_museum_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='museum',
            name='users',
            field=models.ManyToManyField(related_name='museums', to='museos_app.User'),
        ),
    ]