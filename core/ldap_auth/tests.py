from django.test import TestCase
from .models import LDAPConnection


class LDAPConnectionTestCase(TestCase):
    def setUp(self):
        self.ldap_conn = LDAPConnection.objects.create(
            domain_name="example.com",
            domain_controller="dc.example.com",
            username="admin"
        )
        self.ldap_conn.set_password("strong_password")
        self.ldap_conn.save()

    def test_set_password(self):
        self.assertTrue(self.ldap_conn.check_password("strong_password"))
