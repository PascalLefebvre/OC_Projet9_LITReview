from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from itertools import chain
from django.db.models import CharField, Value


@login_required
def home(request):
    return render(request, 'bookreview/home.html')


"""def feed(request):
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    # combine and sort the two types of posts
    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)
    return render(request, 'feed.html', context={'posts': posts})"""


'''
# in feed.html
# Use the 'include' tag to reuse ticket and review elements between pages
...
{% for post in posts %}
    {% if post.content_type == 'TICKET' %}
        {% include 'ticket_snippet.html' %}
    {% elif post.content_type == 'REVIEW' %}
        {% include 'review_snippet.html' %}
{% endfor %}
...
'''

