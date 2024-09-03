from ldap_auth.ldap_utils import connect_to_ldap, get_organizational_units
from ldap_auth.models import LDAPConnection
from django.contrib.auth.models import User


class LDAPService:
    def __init__(self, ldap_conn: LDAPConnection):
        self.conn = connect_to_ldap(ldap_conn)

    def fetch_organizational_units(self):
        if not self.conn:
            raise ValueError("Unable to establish LDAP connection.")

        # Выводим доступные naming contexts для проверки
        print("Available naming contexts:", self.conn.server.info.naming_contexts)

        # Используем первый доступный naming context
        search_base = self.conn.server.info.naming_contexts[0]

        try:
            ous = get_organizational_units(self.conn, search_base)
            return ous
        except Exception as e:
            print(f"Error fetching organizational units: {e}")
            return []

    @staticmethod
    def get_search_base_from_domain(domain_name: str) -> str:
        components = domain_name.split('.')
        base = ','.join([f"dc={comp}" for comp in components])
        return base

    def export_users(self, ous):
        """
        Экспортирует пользователей из выбранных OU в базу данных Django.
        """
        if not self.conn:
            raise ValueError("Unable to establish LDAP connection.")

        for ou in ous:
            self.conn.search(
                search_base=ou,
                search_filter='(objectClass=person)',
                attributes=['cn', 'mail', 'telephoneNumber']
            )

            for entry in self.conn.entries:
                username = entry.cn.value
                email = entry.mail.value
                phone = entry.telephoneNumber.value if entry.telephoneNumber else None

                # Создаем пользователя, если его нет в базе данных
                user, created = User.objects.get_or_create(username=username, defaults={
                    'email': email,
                    'is_active': True,
                })

                if created:
                    user.set_password(User.objects.make_random_password())
                    user.save()
