from django import forms
from django.core.validators import RegexValidator

from .models import Ticket, Review


alphanumeric_plus = RegexValidator(r'^[0-9a-zA-Z_@+.-]*$', 'Uniquement des lettres, nombres et les caractères \
                                                            « @ », « . », « + », « - » et « _ ».')


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {'title': 'Titre'}
        widgets = {'title': forms.TextInput(attrs={'size': '80'}),
                   'description': forms.Textarea(attrs={'cols': 80, 'rows': 8}),
                #    'image': forms.FileInput(attrs={'id': 'Télécharger le fichier'}),
                #    'image': forms.FileInput(attrs={'class': 'btn-secondary'}),
                   }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {'headline': 'Titre', 'rating': 'Note', 'body': 'Commentaire'}
        widgets = {'headline': forms.TextInput(attrs={'size': 80}),
                   'body': forms.Textarea(attrs={'cols': 80, 'rows': 8}),
                   }


class SubscriptionsForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'size': 80, 'placeholder': "Nom d'utilisateur"}),
                               max_length=150, validators=[alphanumeric_plus])
    username.label = ''
