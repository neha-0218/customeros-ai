from django import forms
from .models import RoadmapItem
from features.models import Feature


class RoadmapItemForm(forms.ModelForm):
    class Meta:
        model = RoadmapItem
        fields = ['title', 'description', 'status', 'target_quarter', 'target_year', 'linked_features']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'target_quarter': forms.Select(attrs={'class': 'form-select'}),
            'target_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'linked_features': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        if organization:
            self.fields['linked_features'].queryset = Feature.objects.filter(
                organization_account__organization=organization
            )
        self.fields['linked_features'].required = False