from django import forms

from .models import Ticket, Review, UserFollows


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {'description': forms.Textarea(attrs={'cols': 80})}

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']


class UserFollowsForm(forms.ModelForm):

    class Meta:
        model = UserFollows
        fields = [ 'followed_user', ]
        labels = {'followed_user': ''}
