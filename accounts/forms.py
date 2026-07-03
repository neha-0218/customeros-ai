from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Organization


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    organization_name = forms.CharField(
        max_length=255,
        help_text="Enter your company name. If it doesn't exist yet, we'll create it."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'organization_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']

        org_name = self.cleaned_data['organization_name']
        organization, _ = Organization.objects.get_or_create(name=org_name)
        user.organization = organization

        if commit:
            user.save()
        return user