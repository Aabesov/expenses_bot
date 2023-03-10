# Generated by Django 4.1.7 on 2023-02-17 08:09

from django.db import migrations, models
import django_regex.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0004_alter_profile_external_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(validators=[django_regex.validators.RegexValidator(code='^\\d+ [А-я]+$')], verbose_name='Текст'),
        ),
    ]
