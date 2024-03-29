import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone


class User(AbstractUser):
    uid = models.CharField('Uid', unique=True, default=uuid.uuid4, max_length=36)
    is_agent = models.BooleanField('is Agent', default=False)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE,
                                     related_name='agent_organization', null=True)

    def __str__(self):
        return f'{self.organization.name if self.is_agent else "Normal User"}' \
               f'- {self.username}'



class Organization(models.Model):
    uid = models.CharField('Uid', unique=True, default=uuid.uuid4, max_length=36)
    name = models.CharField('Name', max_length=255, unique=True)
    address = models.CharField('Address', max_length=1000, null=True, blank=True)
    phone = models.CharField('Phone Number', max_length=16, null=True, blank=True)
    description = models.CharField('Description', max_length=1000, null=True, blank=True)

    def __str__(self):
        return '%s' % self.name
