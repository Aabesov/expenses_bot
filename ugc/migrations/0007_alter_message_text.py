# Generated by Django 4.1.7 on 2023-02-17 08:20

from django.db import migrations, models
import ugc.models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0006_alter_message_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(validators=[ugc.models.validate_hash], verbose_name='Текст'),
        ),
    ]
