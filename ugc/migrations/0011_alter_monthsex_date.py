# Generated by Django 4.1.7 on 2023-02-21 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0010_alter_dayex_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthsex',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Время получения'),
        ),
    ]
