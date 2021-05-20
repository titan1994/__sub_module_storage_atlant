from tortoise import fields, models
from MODS.standart_namespace.models import asf


class ORM_nsi_farmerpassport_type_values(models.Model):
    """
    Типы значения (План/Факт)
    """
    __original_dict_name__ = 'type_values'
    __original_client_name__ = 'Farmer passport'

    
    # Наименование
    name = fields.CharField(
        description ='Наименование', max_length=126, pk=True
    )
    
    # Код
    code = fields.IntField(
        description ='Код'
    )
    

    class Meta:
        table = asf('nsi_farmerpassport_type_values')
