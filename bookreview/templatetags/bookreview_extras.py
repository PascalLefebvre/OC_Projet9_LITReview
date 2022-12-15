""" Custom tags and filters. """

from django import template

from bookreview.models import Review

register = template.Library()

@register.filter
def already_reviewed(ticket, user):
    """ Check if the logged user has already responded to the ticket. """
    if Review.objects.filter(ticket=ticket).filter(user=user).exists():
        return True
    else:
        return False

@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    """ Check if the logged user is the author of the post (ticket or review). """
    if user == context['user']:
        return 'Vous'
    return f"{user.username}"
