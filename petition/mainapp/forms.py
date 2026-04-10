from django import forms

class SignatureForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ihr Name (optional)',
            'class': 'form-control'
        })
    )