from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db import IntegrityError
from django.core.paginator import Paginator


from itertools import chain
from django.db.models import CharField, Value
from django.db.models import Q

from .models import Ticket, Review, UserFollows
from accounts.models import User
from .forms import TicketForm, ReviewForm, SubscriptionsForm


def get_followed_users(user):
    """ Get the users that the user follows. """
    followed_users = []
    user_follows_rows = user.following.all()
    for row in user_follows_rows:
        followed_users.append(row.followed_user)
    return followed_users


@login_required
def home(request):
    """The home page for bookreview."""
    # Get the users that the user follows.
    followed_users = get_followed_users(request.user)

    # A queryset of viewable tickets
    tickets = Ticket.objects.filter(Q(user__in=followed_users) | Q(user=request.user))
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    # A queryset of viewable reviews
    reviews = Review.objects.filter(Q(user__in=followed_users) | Q(user=request.user) | Q(ticket__user=request.user))
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    # combine and sort the two types of posts
    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)
    context = {'page_posts': page_posts}
    return render(request, 'bookreview/home.html', context)


@login_required
def new_ticket(request):
    """Add a new ticket."""
    if request.method != 'POST':
        form = TicketForm()
    else:
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            return redirect('bookreview:home')

    context = {'form': form}
    return render(request, 'bookreview/new_ticket.html', context)


@login_required
def edit_ticket(request, ticket_id):
    """Edit a ticket."""
    ticket = Ticket.objects.get(id=ticket_id)

    if ticket.user != request.user:
        raise Http404

    if request.method != 'POST':
        form = TicketForm(instance=ticket)
    else:
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('bookreview:posts')

    context = {'ticket': ticket, 'form': form}
    return render(request, 'bookreview/edit_ticket.html', context)


@login_required
def delete_ticket(request, ticket_id):
    """Delete a ticket."""
    ticket = Ticket.objects.get(id=ticket_id)

    if ticket.user != request.user:
        raise Http404

    if request.method == 'POST':
        ticket.delete()
        return redirect('bookreview:posts')

    context = {'ticket': ticket}
    return render(request, 'bookreview/delete_ticket.html', context)


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
def new_review_one_step(request):
    """ Add a new review that is NOT in response to a ticket.
        Create the ticket and the review at the same time."""
    if request.method != 'POST':
        ticket_form = TicketForm()
        review_form = ReviewForm()
    else:
        ticket_form = TicketForm(request.POST)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            new_ticket = ticket_form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            new_review = review_form.save(commit=False)
            new_review.ticket = new_ticket
            new_review.user = request.user
            new_review.save()
            return redirect('bookreview:home')

    context = {'ticket_form': ticket_form, 'review_form': review_form}
    return render(request, 'bookreview/new_review_one_step.html', context)


@login_required
def edit_review(request, review_id):
    """Edit a review."""
    review = Review.objects.get(id=review_id)

    if review.user != request.user:
        raise Http404

    if request.method != 'POST':
        form = ReviewForm(instance=review)
    else:
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('bookreview:posts')

    context = {'review': review, 'form': form}
    return render(request, 'bookreview/edit_review.html', context)


@login_required
def delete_review(request, review_id):
    """Delete a ticket."""
    review = Review.objects.get(id=review_id)

    if review.user != request.user:
        raise Http404

    if request.method == 'POST':
        review.delete()
        return redirect('bookreview:posts')

    context = {'review': review}
    return render(request, 'bookreview/delete_review.html', context)


@login_required
def posts(request):
    """The user posts page."""
    # A queryset of viewable tickets
    tickets = Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    # A queryset of viewable reviews
    reviews = Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    # combine and sort the two types of posts
    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)
    context = {'page_posts': page_posts}
    return render(request, 'bookreview/posts.html', context)


@login_required
def subscriptions(request):
    """The user subscriptions page."""
    # Get the users that the user follows.
    followed_users = get_followed_users(request.user)

    # Get the logged user's subscribers.
    user_subscribers = []
    users_follows_rows = request.user.followed_by.all()
    for row in users_follows_rows:
        user_subscribers.append(row.user)

    # Subscribe to a user.
    message = ''
    if request.method != 'POST':
        subscription_form = SubscriptionsForm()
    else:
        subscription_form = SubscriptionsForm(request.POST)
        if subscription_form.is_valid():
            try:
                subscribe_username = subscription_form.cleaned_data['username']
                subscribe_user = User.objects.get(username=subscribe_username)
                user_follows = UserFollows(user=request.user, followed_user=subscribe_user)
                user_follows.save()
                return redirect('bookreview:subscriptions')
            except User.DoesNotExist:
                message = "Cet utilisateur n'existe pas."
            except IntegrityError as e:
                if 'CHECK constraint' in str(e):
                    message = "Vous ne pouvez pas vous abonner à vous-même !"
                if 'UNIQUE constraint' in str(e):
                    message = "Vous êtes déjà abonné à cet utilisateur !"

    context = {'message': message, 'subscription_form': subscription_form,
               'followed_users': followed_users, 'user_subscribers': user_subscribers}
    return render(request, 'bookreview/subscriptions.html', context)


@login_required
def unsubscribe_user(request, user_id):
    """Unsubscribe from a user."""
    user_follows = UserFollows.objects.get(user=request.user, followed_user__id=user_id)
    if request.method == 'POST':
        user_follows.delete()
        return redirect('bookreview:subscriptions')
