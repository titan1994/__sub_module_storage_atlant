from tortoise import fields, models
from MODS.standart_namespace.models import asf


class ORM_nsi_general_nsi_new_dict(models.Model):
    """
    супер инфа
    """
    __original_dict_name__ = 'new_dict'
    __original_client_name__ = 'general_nsi'
    
    # ИНН
    INN777 = fields.CharField(
        description ='ИНН', max_length=100, pk=True
    )
    
    # OKTMO
    OKTMO = fields.CharField(
        description ='OKTMO', max_length=100
    )
    

    class Meta:
        table = asf('nsi_general_nsi_new_dict')
