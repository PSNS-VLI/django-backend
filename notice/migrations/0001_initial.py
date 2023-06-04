# Generated by Django 2.2 on 2023-02-04 18:55

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalNotice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('timestamp', models.IntegerField(verbose_name='时间戳')),
                ('title', models.CharField(max_length=20, verbose_name='通知标题')),
                ('content', ckeditor.fields.RichTextField(verbose_name='通知内容')),
                ('origin', models.CharField(choices=[('科大信息', '科大信息'), ('科大拼车', '科大拼车')], max_length=10, verbose_name='通知来源')),
                ('visitor', models.IntegerField(default=0, verbose_name='浏览量')),
            ],
            options={
                'verbose_name': '全局通知',
                'verbose_name_plural': '全局通知',
            },
        ),
        migrations.CreateModel(
            name='PersonalNotice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('timestamp', models.IntegerField(verbose_name='时间戳')),
                ('title', models.CharField(max_length=20, verbose_name='通知标题')),
                ('content', ckeditor.fields.RichTextField(verbose_name='通知内容')),
                ('origin', models.CharField(choices=[('科大信息', '科大信息'), ('科大拼车', '科大拼车')], max_length=10, verbose_name='通知来源')),
            ],
            options={
                'verbose_name': '个人通知',
                'verbose_name_plural': '个人通知',
            },
        ),
    ]
