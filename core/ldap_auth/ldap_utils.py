from ldap3 import Server, Connection, ALL, SIMPLE
from ldap3.core.exceptions import LDAPException, LDAPSocketOpenError, LDAPBindError
from .models import LDAPConnection
from django.core.cache import cache


def connect_to_ldap(ldap_conn: LDAPConnection):
    """
    Подключается к LDAP серверу с использованием данных из модели LDAPConnection.
    Возвращает объект подключения или None в случае ошибки.
    """
    try:
        print(f"Connecting to LDAP with username: {ldap_conn.domain_name.replace('.com', '')}\\{ldap_conn.username}")
        print(f"Password: {ldap_conn.password}")
        server = Server(ldap_conn.domain_controller, get_info=ALL)
        conn = Connection(
            server,
            user=f"{ldap_conn.domain_name.replace('.com', '')}\\{ldap_conn.username}",
            password=ldap_conn.password,
            authentication=SIMPLE,  # Измените NTLM на SIMPLE
            auto_bind=True
        )
        return conn
    except (LDAPException, LDAPSocketOpenError, LDAPBindError) as e:
        print(f"Error connecting to LDAP server: {e}")
        return None


def get_organizational_units(conn, search_base: str):
    """
    Возвращает список организационных единиц (OU) в LDAP.
    """
    cache_key = f"ldap_ous_{search_base}"
    ous = cache.get(cache_key)

    if not ous:
        try:
            conn.search(
                search_base=search_base,
                search_filter='(objectClass=organizationalUnit)',
                search_scope='SUBTREE',
                attributes=['ou']
            )
            ous = conn.entries
            cache.set(cache_key, ous, timeout=3600)  # Кешируем на 1 час
        except LDAPException as e:
            print(f"Error fetching organizational units: {e}")
            ous = []

    return ous
