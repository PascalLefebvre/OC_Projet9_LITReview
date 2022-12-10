"""Defines URL patterns for bookreview."""

from django.urls import path

from . import views

app_name = "bookreview"

urlpatterns = [
    # Home page.
    path("home/", views.home, name="home"),
    path("posts/", views.posts, name="posts"),
    # Page for adding a new ticket.
    path("new_ticket/", views.new_ticket, name="new_ticket"),
    # Page for adding a new review.
    path("new_review/<int:ticket_id>/", views.new_review, name="new_review"),
    # Page for editing a review.
    path("edit_review/<int:review_id>/", views.edit_review, name="edit_review"),
]
