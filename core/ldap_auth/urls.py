from django.urls import path
from .views import list_organizational_units, export_users

urlpatterns = [
    path('ous/<int:ldap_connection_id>/', list_organizational_units, name='ou_list'),
    path('export_users/<int:ldap_connection_id>/', export_users, name='export_users'),
]
