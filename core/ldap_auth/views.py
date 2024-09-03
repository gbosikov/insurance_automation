from django.shortcuts import render, get_object_or_404
from ldap_auth.models import LDAPConnection
from ldap_auth.services.ldap_service import LDAPService
from django.shortcuts import redirect


def list_organizational_units(request, ldap_connection_id):
    ldap_conn = get_object_or_404(LDAPConnection, pk=ldap_connection_id)
    ldap_service = LDAPService(ldap_conn)

    try:
        organizational_units = ldap_service.fetch_organizational_units()
    except Exception as e:
        organizational_units = []
        print(f"Failed to fetch OUs: {e}")

    return render(request, 'ldap_auth/ou_list.html', {
        'ous': organizational_units,
        'ldap_conn': ldap_conn  # Передаем объект соединения в шаблон
    })


def export_users(request, ldap_connection_id):
    ldap_conn = get_object_or_404(LDAPConnection, pk=ldap_connection_id)
    ldap_service = LDAPService(ldap_conn)

    selected_ous = request.POST.getlist('ous')
    ldap_service.export_users(selected_ous)

    return redirect('ou_list', ldap_connection_id=ldap_connection_id)
