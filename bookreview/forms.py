from django import forms

from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {'description': forms.Textarea(attrs={'cols': 80})}

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']


class SubscriptionsForm(forms.Form):
    username = forms.CharField(max_length=150)
