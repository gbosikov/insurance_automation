from .ldap_utils import connect_to_ldap, get_organizational_units
from .models import LDAPConnection


class LDAPService:
    def __init__(self, ldap_conn: LDAPConnection):
        self.conn = connect_to_ldap(ldap_conn)

    def fetch_organizational_units(self):
        if not self.conn:
            raise ValueError("Unable to establish LDAP connection.")

        search_base = self.get_search_base_from_domain(self.conn.server.info.server_name)
        return get_organizational_units(self.conn, search_base)

    @staticmethod
    def get_search_base_from_domain(domain_name: str) -> str:
        components = domain_name.split('.')
        base = ','.join([f"dc={comp}" for comp in components])
        return base
