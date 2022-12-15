from django import forms
from django.core.validators import RegexValidator

from .models import Ticket, Review


alphanumeric_plus = RegexValidator(r'^[0-9a-zA-Z_@+.-]*$', 'Seuls les caractères alphanumériques (sans accent) \
                                                            et "_ @ + . -" sont autorisés.')


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
    username = forms.CharField(max_length=150, validators=[alphanumeric_plus])
