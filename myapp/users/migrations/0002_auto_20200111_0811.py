# Generated by Django 2.2.4 on 2020-01-11 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='superuser',
        ),
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='1', max_length=50),
            preserve_default=False,
        ),
    ]
