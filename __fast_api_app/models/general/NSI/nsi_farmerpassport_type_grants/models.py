from tortoise import fields, models
from MODS.standart_namespace.models import asf


class ORM_nsi_farmerpassport_type_grants(models.Model):
    """
    Виды гранта
    """
    __original_dict_name__ = 'type_grants'
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
        table = asf('nsi_farmerpassport_type_grants')
