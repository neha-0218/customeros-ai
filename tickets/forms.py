from django import forms
from .models import Ticket
from accounts.models import CustomerAccount
from features.models import Feature


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['customer_account', 'subject', 'description', 'priority', 'category', 'linked_feature']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'customer_account': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'linked_feature': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        if organization:
            self.fields['customer_account'].queryset = CustomerAccount.objects.filter(
                organization=organization
            )
        self.fields['linked_feature'].required = False
        self.fields['linked_feature'].queryset = Feature.objects.all()