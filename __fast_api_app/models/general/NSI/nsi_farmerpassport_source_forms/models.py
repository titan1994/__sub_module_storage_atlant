from tortoise import fields, models
from MODS.standart_namespace.models import asf


class ORM_nsi_farmerpassport_source_forms(models.Model):
    """
    Формы источника
    """
    __original_dict_name__ = 'source_forms'
    __original_client_name__ = 'Farmer passport'

    
    # Наименование
    name = fields.CharField(
        description ='Наименование', max_length=126, pk=True
    )
    
    # Код
    code = fields.IntField(
        description ='Код'
    )
    
    # Приоритет
    property = fields.IntField(
        description ='Приоритет'
    )
    

    class Meta:
        table = asf('nsi_farmerpassport_source_forms')
