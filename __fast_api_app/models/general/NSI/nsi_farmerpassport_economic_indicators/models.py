from tortoise import fields, models
from MODS.standart_namespace.models import asf


class ORM_nsi_farmerpassport_economic_indicators(models.Model):
    """
    Экономические показатели
    """
    __original_dict_name__ = 'economic_indicators'
    __original_client_name__ = 'Farmer passport'

    
    # Наименование
    name = fields.TextField(
        description ='Наименование', pk=True
    )
    
    # Код
    code = fields.IntField(
        description ='Код'
    )
    
    # Номер по порядку
    npp = fields.IntField(
        description ='Номер по порядку'
    )
    
    # Родитель
    parent = fields.TextField(
        description ='Родитель'
    )
    

    class Meta:
        table = asf('nsi_farmerpassport_economic_indicators')
