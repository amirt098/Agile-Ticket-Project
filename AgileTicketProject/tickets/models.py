import uuid

from django.db import models
try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone


class PreSetReply(models.Model):
    uid = models.CharField('Uid', unique=True,  max_length=36, default=uuid.uuid4)
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


class Product(models.Model):
    uid = models.CharField('Uid', unique=True, default=uuid.uuid4, max_length=36)
    name = models.CharField('Name', max_length=100)
    owner = models.CharField("Organization Uid",  max_length=36)
    pre_set_reply = models.CharField("Pre Set Reply", max_length=200, null=True)
    description = models.CharField("Description", max_length=500, null=True, blank=True)
    image = models.ImageField('Image', upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        unique_together = ('owner', 'name')

    def __str__(self):
        return self.name


class Ticket(models.Model):
    uid = models.CharField('Uid', unique=True, default=uuid.uuid4, max_length=36)
    title = models.CharField('Title', max_length=255)
    owner = models.CharField(blank=True, null=False, verbose_name='Owner user uid',  max_length=36)
    description = models.TextField('Description', blank=True, null=True,  max_length=500)
    product_uid = models.CharField('Product_Uid', null=True, max_length=36)

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
                              max_length=50,
                              blank=True,
                              null=True)
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=MEDIUM)
    closed_date = models.DateTimeField(blank=True, null=True)
    assigned_to = models.CharField(verbose_name='Assign to User',
                                   blank=True,
                                   null=True,  max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FollowUp(models.Model):
    """
    A FollowUp is a comment to a ticket.
    """
    ticket_uid = models.CharField('Ticket_uid', max_length=36, null=True)
    date = models.DateTimeField('Date', default=timezone.now)
    title = models.CharField('Title', max_length=200)
    text = models.TextField('Text', blank=True, null=True,  max_length=500)
    user = models.CharField(blank=True, null=True, verbose_name='User - Uid',  max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified_at', ]


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
    ticket = models.ForeignKey(Ticket, verbose_name='Ticket', on_delete=models.CASCADE)
    file = models.FileField('File', upload_to=attachment_path, max_length=1000)
    filename = models.CharField('Filename', max_length=1000)
    user = models.CharField(blank=True, null=True, verbose_name='User Uid',  max_length=36)
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
