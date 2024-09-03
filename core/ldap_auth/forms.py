from django import forms
from .models import LDAPConnection


class LDAPConnectionForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = LDAPConnection
        fields = ['domain_name', 'domain_controller', 'username', 'password']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data["password"]:
            instance.set_password(self.cleaned_data["password"])
        if commit:
            instance.save()
        return instance

    def clean_domain_name(self):
        domain_name = self.cleaned_data.get('domain_name')
        if not domain_name or "." not in domain_name:
            raise forms.ValidationError("Invalid domain name format.")
        return domain_name
