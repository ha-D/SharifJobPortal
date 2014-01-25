from django.forms import forms
from jobs.models import JobOpportunity

class JobForm(forms.ModelForm):
    class Meta:
        model = JobOpportunity
        fields = ['name', 'sex', 'baseSalary', 'number', 'expireDate']
