""" Custom tags and filters. """

from django import template

from bookreview.models import Review
from django.utils.safestring import mark_safe

MAX_RATING = 5

register = template.Library()

@register.filter
def already_reviewed(ticket, user):
    """ Check if the logged user has already responded to the ticket. """
    if Review.objects.filter(ticket=ticket).filter(user=user).exists():
        return True
    else:
        return False

@register.filter
def display_stars_rating(rating):
    """ Change the rating display from integer to stars. """
    string = ''
    for i in range(rating):
        string += '  ' + '<span class="bi bi-star-fill fw-bold"></span>'
    for i in range(rating, MAX_RATING):
        string += '  ' + '<span class="bi bi-star fw-bold"></span>'
    return mark_safe(string)

@register.simple_tag(takes_context=True)
def get_post_author(context, user):
    """ Return the author of the post (ticket or review). """
    if user == context['user']:
        return 'Vous'
    return f"{user.username}"
