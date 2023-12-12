# Generated by Django 3.2.12 on 2023-12-12 14:04

import apps.tickets.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PreSetReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=36, unique=True, verbose_name='Uid')),
                ('name', models.CharField(help_text='Only used to assist users with selecting a reply - not shown to the user.', max_length=100, verbose_name='Name')),
                ('body', models.TextField(help_text='Context available: {{ ticket }} - ticket object (eg {{ ticket.title }}); {{ queue }} - The queue; and {{ user }} - the current user.', verbose_name='Body')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('owner', models.CharField(blank=True, max_length=36, null=True, verbose_name='Owner user uid')),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Description')),
                ('status', models.CharField(blank=True, choices=[(1, 'Open'), (2, 'Reopened'), (3, 'Resolved'), (4, 'Closed')], max_length=50, null=True, verbose_name='Status')),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium', max_length=20)),
                ('closed_date', models.DateTimeField(blank=True, null=True)),
                ('assigned_to', models.CharField(blank=True, max_length=36, null=True, verbose_name='Assign to User')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=36, unique=True, verbose_name='Uid')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('owner', models.CharField(max_length=36, verbose_name='Organization Uid')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Description')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Image')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('pre_set_reply', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.presetreply')),
            ],
        ),
        migrations.CreateModel(
            name='FollowUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('text', models.TextField(blank=True, max_length=500, null=True, verbose_name='Text')),
                ('user', models.CharField(blank=True, max_length=36, null=True, verbose_name='User - Uid')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.ticket', verbose_name='Ticket')),
            ],
            options={
                'ordering': ['-modified_at'],
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=1000, upload_to=apps.tickets.models.attachment_path, verbose_name='File')),
                ('filename', models.CharField(max_length=1000, verbose_name='Filename')),
                ('user', models.CharField(blank=True, max_length=36, null=True, verbose_name='User Uid')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.ticket', verbose_name='Ticket')),
            ],
            options={
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachments',
            },
        ),
    ]
