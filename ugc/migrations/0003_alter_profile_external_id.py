# Generated by Django 4.1.7 on 2023-02-16 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0002_alter_profile_options_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='external_id',
            field=models.PositiveSmallIntegerField(unique=True, verbose_name='ID пользователя в соц сети'),
        ),
    ]