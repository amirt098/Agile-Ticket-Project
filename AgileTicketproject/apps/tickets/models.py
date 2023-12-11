from django.db import models
from django.contrib.auth.models import User, AbstractUser

try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone


def user_unicode(self):
    """
    return 'last_name, first_name' for User by default
    """
    return u'%s, %s' % (self.last_name, self.first_name)


User.__unicode__ = user_unicode


class User(AbstractUser):
    pass
    # Todo: add uid to models?


class Agent(AbstractUser):
    role = models.ForeignKey('Role', null=True)


class Role(models.Model):
    name = models.CharField('Name', max_length=100)
    description = models.CharField('Description')


class PreSetReply(models.Model):
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
    name = models.CharField('Name', max_length=255)
    Address = models.CharField('Address', max_length=1000, null=True, blank=True)
    phone = models.IntegerField('Phone Number', max_length=16, null=True)
    description = models.CharField('Description', max_length=1000, null=True, blank=True)
    users = models.ManyToManyField(User, null=True)
    pre_set_replies = models.ManyToManyField(PreSetReply, null=True)


class Product(models.Model):
    name = models.CharField('Name', max_length=100)
    owner = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="Producer")
    description = models.CharField("Description", max_length=500, null=True, blank=True)
    image = models.ImageField('Image', upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    title = models.CharField('Title', max_length=255)
    owner = models.ForeignKey(User,
                              related_name='owner',
                              blank=True,
                              null=True,
                              verbose_name='Owner')
    description = models.TextField('Description', blank=True, null=True)
    STATUS_CHOICES = (
        ('TODO', 'TODO'),
        ('IN PROGRESS', 'IN PROGRESS'),
        ('WAITING', 'WAITING'),
        ('DONE', 'DONE'),
    )
    OPEN_STATUS = 1
    REOPENED_STATUS = 2
    RESOLVED_STATUS = 3
    CLOSED_STATUS = 4
    DUPLICATE_STATUS = 5
    STATUS_CHOICES = (
        (OPEN_STATUS, 'Open'),
        (REOPENED_STATUS, 'Reopened'),
        (RESOLVED_STATUS, 'Resolved'),
        (CLOSED_STATUS, 'Closed'),
    )
    status = models.CharField('Status',
                              choices=STATUS_CHOICES,
                              max_length=255,
                              blank=True,
                              null=True)
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICALITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]
    priority = models.CharField(max_length=20, choices=CRITICALITY_CHOICES, default=LOW)
    waiting_for = models.ForeignKey(User,
                                    related_name='waiting_for',
                                    blank=True,
                                    null=True,
                                    verbose_name='Waiting For')
    closed_date = models.DateTimeField(blank=True, null=True)
    assigned_to = models.ForeignKey(User,
                                    related_name='assigned_to',
                                    blank=True,
                                    null=True,
                                    verbose_name='Assigned to')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id)


class FollowUp(models.Model):
    """
    A FollowUp is a comment to a ticket.
    """
    ticket = models.ForeignKey(Ticket, verbose_name='Ticket')
    date = models.DateTimeField('Date', default=timezone.now)
    title = models.CharField('Title', max_length=200, )
    text = models.TextField('Text', blank=True, null=True, )
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='User')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified', ]


def attachment_path(instance, filename):
    """
    Provide a file path that will help prevent files being overwritten, by
    putting attachments in a folder off attachments for ticket/followup_id/.
    """
    import os
    from django.conf import settings
    os.umask(0)
    path = 'tickets/%s' % instance.ticket.id
    print(path)
    att_path = os.path.join(settings.MEDIA_ROOT, path)
    if settings.DEFAULT_FILE_STORAGE == "django.core.files. \
                                         storage.FileSystemStorage":
        if not os.path.exists(att_path):
            os.makedirs(att_path, 0o777)
    return os.path.join(path, filename)


class Attachment(models.Model):
    ticket = models.ForeignKey(Ticket, verbose_name='Ticket')
    file = models.FileField('File',
                            upload_to=attachment_path,
                            max_length=1000)
    filename = models.CharField('Filename', max_length=1000)
    user = models.ForeignKey(User,
                             blank=True,
                             null=True,
                             verbose_name='User')
    created = models.DateTimeField(auto_now_add=True)

    def get_upload_to(self, field_attname):
        """ Get upload_to path specific to this item """
        if not self.id:
            return u''
        return u'../media/tickets/%s' % (
            self.ticket.id,
        )

    class Meta:
        # ordering = ['filename', ]
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'
