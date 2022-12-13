"""Defines URL patterns for bookreview."""

from django.urls import path

from . import views

app_name = "bookreview"

urlpatterns = [
    # Home page.
    path("", views.home, name="home"),
    # Page for viewing the user posts.
    path("posts/", views.posts, name="posts"),
    # Page for viewing the user subscriptions.
    path("subscriptions/", views.subscriptions, name="subscriptions"),
    # Page for adding a new ticket.
    path("new_ticket/", views.new_ticket, name="new_ticket"),
    # Page for editing a ticket.
    path("edit_ticket/<int:ticket_id>/", views.edit_ticket, name="edit_ticket"),
    # Page for deleting a ticket.
    path("delete_ticket/<int:ticket_id>/", views.delete_ticket, name="delete_ticket"),
    # Page for adding a new review in response to a ticket.
    path("new_review/<int:ticket_id>/", views.new_review, name="new_review"),
    # Page for adding a new review in one step (create the ticket in the same time).
    path("new_review_one_step/", views.new_review_one_step, name="new_review_one_step"),
    # Page for editing a review.
    path("edit_review/<int:review_id>/", views.edit_review, name="edit_review"),
    # Page for deleting a review.
    path("delete_review/<int:review_id>/", views.delete_review, name="delete_review"),
]
