# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-18 19:11
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('type', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Company ID')),
                ('name', models.CharField(max_length=50, verbose_name='Company name')),
                ('phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone number')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Category', verbose_name='Category')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Eligibility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Department', verbose_name='Department')),
            ],
        ),
        migrations.CreateModel(
            name='JAF',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='JAF no.')),
                ('description', models.TextField(verbose_name='Job description')),
                ('other_details', models.TextField(blank=True, null=True, verbose_name='Other details')),
                ('requirements', models.TextField(verbose_name='Job requirements')),
                ('job_year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1958)], verbose_name='Internship year')),
                ('job_season', models.IntegerField(choices=[(0, 'Winter'), (1, 'Summer')], verbose_name='Job Season')),
                ('posting', models.CharField(max_length=50, verbose_name='Place of posting')),
                ('accomodation', models.TextField(verbose_name='Accomodation details')),
                ('duration', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Internship duration (weeks)')),
                ('resume_number', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)], verbose_name='Resume no. wanted')),
                ('cpi_cutoff', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)], verbose_name='CPI')),
                ('stipend', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Stipend')),
                ('deadline', models.DateTimeField(verbose_name='Last date to sign JAF')),
                ('currency', models.CharField(default='INR', max_length=3, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(3)], verbose_name='Unit')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Company', verbose_name='Company')),
            ],
        ),
        migrations.CreateModel(
            name='JAFTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_number', models.IntegerField(verbose_name='Test no.')),
                ('location', models.CharField(blank=True, max_length=50, null=True, verbose_name='Test venue/URL')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='Test time')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Test details')),
                ('duration', models.FloatField(verbose_name='Test duration (minutes)')),
                ('jaf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.JAF', verbose_name='JAF')),
            ],
        ),
        migrations.CreateModel(
            name='JobProfile',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Job profile')),
            ],
        ),
        migrations.CreateModel(
            name='TestType',
            fields=[
                ('type', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Test type')),
            ],
        ),
        migrations.AddField(
            model_name='jaftest',
            name='test_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.TestType', verbose_name='Test type'),
        ),
        migrations.AddField(
            model_name='jaf',
            name='profile',
            field=models.ManyToManyField(to='company.JobProfile', verbose_name='Job profile'),
        ),
        migrations.AddField(
            model_name='eligibility',
            name='jaf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.JAF', verbose_name='JAF'),
        ),
        migrations.AddField(
            model_name='eligibility',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Program', verbose_name='Program'),
        ),
        migrations.AlterUniqueTogether(
            name='jaftest',
            unique_together=set([('test_number', 'jaf')]),
        ),
        migrations.AlterUniqueTogether(
            name='eligibility',
            unique_together=set([('department', 'jaf', 'program')]),
        ),
    ]
