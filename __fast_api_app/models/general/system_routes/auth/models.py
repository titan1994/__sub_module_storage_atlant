from tortoise import fields, models
from MODS.standart_namespace.models import asf


class User(models.Model):
    """
    Пользователь
    """
    username = fields.CharField(max_length=128)
    hashed_password = fields.CharField(max_length=128)
    disabled = fields.BooleanField(default=False)
    class Meta:
        table = asf('user')


class Token(models.Model):
    """
    Пользователь
    """
    username = fields.CharField(max_length=128)
    token = fields.CharField(max_length=256)
    is_active = fields.BooleanField(default=True)
    date_create = fields.DateField(auto_now_add=True, null=True)
    class Meta:
        table = asf('token')