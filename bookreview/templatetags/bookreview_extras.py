""" Custom tags and filters. """

from django import template

from bookreview.models import Ticket, Review

register = template.Library()

@register.filter
def already_reviewed(ticket, user):
    if Review.objects.filter(ticket=ticket).filter(user=user).exists():
        return True
    else:
        return False
