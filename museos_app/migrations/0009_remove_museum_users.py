# Generated by Django 3.2.4 on 2021-07-19 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos_app', '0008_auto_20210719_0109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='museum',
            name='users',
        ),
    ]
