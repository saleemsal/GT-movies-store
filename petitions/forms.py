from django import forms
from .models import Petition

class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['title', 'suggested_movie_title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4})
        }
