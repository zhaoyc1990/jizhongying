# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-08 06:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('host', '0009_hostinfo_host_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigureFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conf_context', models.TextField(blank=True, null=True, verbose_name='\u914d\u7f6e\u6587\u4ef6\u5185\u5bb9')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4fee\u6539\u65e5\u671f')),
                ('createdate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u521b\u5efa/\u6dfb\u52a0\u65e5\u671f')),
                ('conf_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conf_for_group', to='host.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('env_name', models.CharField(max_length=50, verbose_name='\u73af\u5883\u540d')),
                ('env_tag', models.CharField(max_length=50, verbose_name='\u73af\u5883\u7248\u672c')),
                ('is_image', models.BooleanField(default=False, verbose_name='\u662f\u5426\u662f\u955c\u50cf')),
                ('image', models.CharField(blank=True, max_length=80, null=True, verbose_name='\u955c\u50cf\u5b58\u653e\u5730\u5740')),
                ('filepath', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u73af\u5883\u6240\u9700\u6587\u4ef6\u5730\u5740\uff08\u76f8\u5bf9\u7f51\u7ad9\u6839\u76ee\u5f55\uff09')),
                ('env_status', models.BooleanField(default=True, verbose_name='\u955c\u50cf\u662f\u5426\u8fd8\u5728\u4ed3\u5e93\u91cc\u9762')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4fee\u6539\u65e5\u671f')),
                ('createdate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u521b\u5efa/\u6dfb\u52a0\u65e5\u671f')),
                ('env_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='env_group', to='host.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_chinese', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u670d\u52a1\u4e2d\u6587\u540d')),
                ('server_english', models.CharField(max_length=50, verbose_name='\u670d\u52a1\u82f1\u6587\u540d')),
                ('is_container', models.BooleanField(default=False, verbose_name='\u670d\u52a1\u662f\u5426\u5728\u5bb9\u5668\u91cc')),
                ('port', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u670d\u52a1\u7aef\u53e3')),
                ('gitsite', models.CharField(blank=True, max_length=80, null=True, verbose_name='GIT\u4ed3\u5e93\u5730\u5740')),
                ('container_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u5bb9\u5668ID')),
                ('server_status', models.BooleanField(default=True, verbose_name='\u5bb9\u5668\u72b6\u6001')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4fee\u6539\u65e5\u671f')),
                ('createdate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u521b\u5efa/\u6dfb\u52a0\u65e5\u671f')),
                ('server_environment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='environment_id', to='server.Environment')),
                ('server_host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host_pid', to='host.hostinfo')),
            ],
        ),
        migrations.AddField(
            model_name='configurefile',
            name='conf_server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conf_for_server', to='server.Server'),
        ),
    ]
