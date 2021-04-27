from tortoise import fields, models
from MODS.standart_namespace.models import asf


class ExampleModel(models.Model):
    """
    Example model
    """

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)

    class Meta:
        table = asf('example_tortoise_orm')
