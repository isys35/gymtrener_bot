# Generated by Django 3.2.6 on 2021-10-20 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0014_auto_20211018_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='exersice',
            name='details_url',
            field=models.URLField(blank=True, max_length=100),
        ),
    ]
