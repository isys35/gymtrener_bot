# Generated by Django 3.2.6 on 2021-09-14 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0006_exersice'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseUse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webhook.exersice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webhook.telegramuser')),
            ],
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_index', models.IntegerField(default=1)),
                ('repeat', models.IntegerField(default=0)),
                ('mass', models.IntegerField(default=0)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sets', to='webhook.exerciseuse')),
            ],
        ),
    ]
