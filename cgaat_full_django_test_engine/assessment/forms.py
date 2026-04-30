from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'section', 'text', 'skill_tag', 'order',
            'option_a', 'score_a',
            'option_b', 'score_b',
            'option_c', 'score_c',
            'option_d', 'score_d'
        ]
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'skill_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'option_a': forms.TextInput(attrs={'class': 'form-control'}),
            'score_a': forms.NumberInput(attrs={'class': 'form-control'}),
            'option_b': forms.TextInput(attrs={'class': 'form-control'}),
            'score_b': forms.NumberInput(attrs={'class': 'form-control'}),
            'option_c': forms.TextInput(attrs={'class': 'form-control'}),
            'score_c': forms.NumberInput(attrs={'class': 'form-control'}),
            'option_d': forms.TextInput(attrs={'class': 'form-control'}),
            'score_d': forms.NumberInput(attrs={'class': 'form-control'}),
        }
