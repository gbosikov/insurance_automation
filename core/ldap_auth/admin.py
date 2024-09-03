from django.contrib import admin
from .models import LDAPConnection
from .forms import LDAPConnectionForm


class LDAPConnectionAdmin(admin.ModelAdmin):
    form = LDAPConnectionForm
    list_display = ['domain_name', 'username']


admin.site.register(LDAPConnection, LDAPConnectionAdmin)
