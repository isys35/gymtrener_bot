# Generated by Django 3.2.6 on 2021-09-14 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0008_auto_20210914_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exerciseuse',
            name='date_start',
            field=models.DateTimeField(auto_created=True, blank=True, null=True),
        ),
    ]
