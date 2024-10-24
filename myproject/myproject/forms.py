from django import forms
from App.models import Registration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            'name', 'mother_name', 'father_name', 'adhar_card', 'gender',
            'street', 'colony', 'city', 'postal_code', 'state', 'country',
            'email', 'mobile', 'password', 'username', 'photo'
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }
