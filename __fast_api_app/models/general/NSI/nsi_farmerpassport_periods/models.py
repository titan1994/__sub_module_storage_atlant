from tortoise import fields, models
from MODS.standart_namespace.models import asf


class ORM_nsi_farmerpassport_periods(models.Model):
    """
    Периоды
    """
    __original_dict_name__ = 'periods'
    __original_client_name__ = 'Farmer passport'

    
    # Наименование
    name = fields.CharField(
        description ='Наименование', max_length=255, pk=True
    )
    
    # Код
    code = fields.IntField(
        description ='Код'
    )
    

    class Meta:
        table = asf('nsi_farmerpassport_periods')
