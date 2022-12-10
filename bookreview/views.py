from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404


from itertools import chain
from django.db.models import CharField, Value
from django.db.models import Q

from .models import Ticket, Review
from .forms import TicketForm, ReviewForm


@login_required
# @permission_required('bookreview.view_ticket', raise_exception=True)
def home(request):
    """The home page for bookreview."""
    # Get the users that the user follows.
    followed_users = []
    users_follows = request.user.following.all()
    for user_follow in users_follows:
        followed_users.append(user_follow.followed_user)

    # A queryset of viewable tickets
    tickets = Ticket.objects.filter(Q(user__in=followed_users) | Q(user=request.user))
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    # A queryset of viewable reviews
    reviews = Review.objects.filter(Q(user__in=followed_users) | Q(user=request.user) | Q(ticket__user=request.user))
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    # combine and sort the two types of posts
    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)
    return render(request, 'bookreview/home.html', context={'posts': posts})

@login_required
# @permission_required('bookreview.add_ticket', raise_exception=True)
def new_ticket(request):
    """Add a new ticket."""
    if request.method != 'POST':
        form = TicketForm()
    else:
        form = TicketForm(request.POST)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            return redirect('bookreview:home')
    context = {'form': form}
    return render(request, 'bookreview/new_ticket.html', context)

@login_required
def new_review(request, ticket_id):
    """Add a new review in response to a ticket."""
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method != 'POST':
        form = ReviewForm()
    else:
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.ticket = ticket
            new_review.user = request.user
            new_review.save()
            return redirect('bookreview:home')

    context = {'ticket': ticket, 'form': form}
    return render(request, 'bookreview/new_review.html', context)

@login_required
def edit_review(request, review_id):
    """Edit a new review."""
    review = Review.objects.get(id=review_id)

    if review.user != request.user:
        raise Http404

    if request.method != 'POST':
        form = ReviewForm(instance=review)
    else:
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('bookreview:home')

    context = {'review': review, 'form': form}
    return render(request, 'bookreview/edit_review.html', context)

@login_required
def posts(request):
    return render(request, 'bookreview/posts.html')
