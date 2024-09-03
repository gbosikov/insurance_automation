from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class LDAPConnection(models.Model):
    domain_name = models.CharField(max_length=255)
    domain_controller = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  # Зашифрованный пароль

    def set_password(self, raw_password: str):
        """
        Сохраняет зашифрованный пароль в базе данных.
        """
        self._password = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """
        Проверяет, совпадает ли введённый пароль с сохранённым.
        """
        return check_password(raw_password, self._password)

    def __str__(self):
        return f"{self.domain_name} - {self.username}"

    def get_connection_credentials(self):
        """
        Возвращает имя пользователя и зашифрованный пароль для подключения.
        Пароль не может быть расшифрован и используется в хэшированном виде.
        """
        return {
            'user': f"{self.domain_name}\\{self.username}",
            'password': self._password
        }
