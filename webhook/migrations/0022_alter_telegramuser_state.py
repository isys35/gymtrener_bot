# Generated by Django 3.2.6 on 2022-01-27 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0021_auto_20220127_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='state',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='webhook.state'),
        ),
    ]