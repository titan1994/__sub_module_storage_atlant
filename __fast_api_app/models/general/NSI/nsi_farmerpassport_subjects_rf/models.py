from tortoise import fields, models
from MODS.standart_namespace.models import asf


class ORM_nsi_farmerpassport_subjects_rf(models.Model):
    """
    Субъекты РФ
    """
    __original_dict_name__ = 'subjects_rf'
    __original_client_name__ = 'Farmer passport'

    
    # Наименование
    name = fields.CharField(
        description ='Наименование', max_length=255, pk=True
    )
    
    # Код
    code = fields.IntField(
        description ='Код'
    )
    
    # Федеральный округ
    federal_district = fields.CharField(
        description ='Федеральный округ', max_length=255
    )
    
    # ОКТМО
    OKTMO = fields.CharField(
        description ='ОКТМО', max_length=255
    )
    

    class Meta:
        table = asf('nsi_farmerpassport_subjects_rf')
