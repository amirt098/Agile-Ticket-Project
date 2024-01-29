from django import template
from django.utils import timezone

register = template.Library()

@register.simple_tag
def current_time():
    return timezone.now()