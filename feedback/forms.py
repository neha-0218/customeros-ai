from django import forms
from .models import Feedback
from accounts.models import CustomerAccount


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['customer_account', 'content', 'source']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'customer_account': forms.Select(attrs={'class': 'form-select'}),
            'source': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        if organization:
            self.fields['customer_account'].queryset = CustomerAccount.objects.filter(
                organization=organization
            )