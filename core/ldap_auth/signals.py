from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LDAPConnection
from .services.ldap_service import LDAPService


@receiver(post_save, sender=LDAPConnection)
def test_ldap_connection(sender, instance, **kwargs):
    try:
        ldap_service = LDAPService(instance)
        ous = ldap_service.fetch_organizational_units()
        # Логируем результат или отправляем уведомление администратору
        print(f"Fetched OUs: {ous}")
    except Exception as e:
        # Логируем ошибку или отправляем уведомление
        print(f"Failed to fetch OUs: {e}")
