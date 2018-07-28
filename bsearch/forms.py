from django import forms

from .models import SearchHistory

class Query(forms.ModelForm):
    class Meta:
        model = SearchHistory
        fields =[
            'queries',

        ]
