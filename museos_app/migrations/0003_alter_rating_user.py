# Generated by Django 3.2.4 on 2021-07-16 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('museos_app', '0002_alter_museum_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='museos_app.user'),
        ),
    ]