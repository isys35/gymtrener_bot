# Generated by Django 3.2.6 on 2021-10-30 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0016_alter_exerciseuse_date_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exersice',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]