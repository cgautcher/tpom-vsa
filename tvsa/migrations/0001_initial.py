# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GroupShift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_shift_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job', models.CharField(max_length=100)),
                ('heavy_lifting', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=100)),
                ('manager', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('notes', models.TextField(blank=True)),
                ('present_for_shift', models.BooleanField(default=False)),
                ('group_shift', models.ForeignKey(related_name='shifts', on_delete=django.db.models.deletion.SET_DEFAULT, default=None, blank=True, to='tvsa.GroupShift', null=True)),
                ('job', models.ForeignKey(related_name='shifts', to='tvsa.Job')),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=12, blank=True)),
                ('seller_number', models.CharField(max_length=100, blank=True)),
                ('role', models.ForeignKey(related_name='volunteers', to='tvsa.Role')),
            ],
        ),
        migrations.AddField(
            model_name='shift',
            name='managers_in_charge',
            field=models.ManyToManyField(to='tvsa.Volunteer'),
        ),
        migrations.AddField(
            model_name='shift',
            name='volunteer',
            field=models.ForeignKey(related_name='shifts', to='tvsa.Volunteer'),
        ),
        migrations.AlterUniqueTogether(
            name='volunteer',
            unique_together=set([('first_name', 'last_name', 'seller_number')]),
        ),
    ]
