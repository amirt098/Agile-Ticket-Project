from django.db import models
from django.contrib.auth.models import User, AbstractUser

try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone


class User(AbstractUser):
    uid = models.CharField('Uid', unique=True)
    pass

class Agent(AbstractUser):
    uid = models.CharField('Uid', unique=True)
    organization = models.CharField('Organization Uid')
    role = models.ForeignKey('Role', null=True)


class Role(models.Model):
    uid = models.CharField('Uid', unique=True)
    name = models.CharField('Name', max_length=100)
    description = models.CharField('Description')


class PreSetReply(models.Model):
    uid = models.CharField('Uid', unique=True)
    name = models.CharField(
        'Name',
        max_length=100,
        help_text='Only used to assist users with selecting a reply - not '
                  'shown to the user.',
    )

    body = models.TextField(
        'Body',
        help_text='Context available: {{ ticket }} - ticket object (eg '
                  '{{ ticket.title }}); {{ queue }} - The queue; and {{ user }} '
                  '- the current user.',
    )

    def __str__(self):
        return '%s' % self.name


class Organization(models.Model):
    uid = models.CharField('Uid', unique=True)
    name = models.CharField('Name', max_length=255)
    Address = models.CharField('Address', max_length=1000, null=True, blank=True)
    phone = models.IntegerField('Phone Number', max_length=16, null=True)
    description = models.CharField('Description', max_length=1000, null=True, blank=True)
    pre_set_replies = models.ManyToManyField(PreSetReply, null=True)

