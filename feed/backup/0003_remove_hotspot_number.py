# Generated by Django 2.2 on 2022-05-11 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_auto_20220511_1421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feed',
            name='number',
        ),
    ]
