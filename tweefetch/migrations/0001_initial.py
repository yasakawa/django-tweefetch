# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-10-08 23:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ListQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fetch_interval_secs', models.IntegerField(default=600, verbose_name='Fetch interval secs')),
                ('save_rts', models.BooleanField(default=False, verbose_name='Save retweets')),
                ('max_fetched_id', models.BigIntegerField(blank=True, null=True, verbose_name='Max fetched TweetID')),
                ('last_fetched_at', models.DateTimeField(blank=True, null=True, verbose_name='Last fetched at')),
                ('error', models.TextField(blank=True, help_text='When a problem occurs', null=True, verbose_name='Error')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('list_id', models.BigIntegerField(blank=True, null=True, verbose_name='List ID')),
                ('slug', models.CharField(blank=True, max_length=30, null=True, verbose_name='Slug')),
                ('owner_id', models.BigIntegerField(blank=True, null=True, verbose_name='Owner ID')),
                ('owner_screen_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Owner screen name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SearchQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fetch_interval_secs', models.IntegerField(default=600, verbose_name='Fetch interval secs')),
                ('save_rts', models.BooleanField(default=False, verbose_name='Save retweets')),
                ('max_fetched_id', models.BigIntegerField(blank=True, null=True, verbose_name='Max fetched TweetID')),
                ('last_fetched_at', models.DateTimeField(blank=True, null=True, verbose_name='Last fetched at')),
                ('error', models.TextField(blank=True, help_text='When a problem occurs', null=True, verbose_name='Error')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('q', models.CharField(max_length=500, verbose_name='Query')),
                ('geocode', models.CharField(blank=True, max_length=50, null=True, verbose_name='Geocode')),
                ('lang', models.CharField(blank=True, max_length=10, null=True, verbose_name='Lang')),
                ('locale', models.CharField(blank=True, max_length=10, null=True, verbose_name='Locale')),
                ('result_type', models.CharField(choices=[('mixed', 'mixed'), ('recent', 'recent'), ('popular', 'popular')], default='recent', max_length=8, verbose_name='Result type')),
                ('include_entities', models.BooleanField(default=False, verbose_name='Include entities')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]