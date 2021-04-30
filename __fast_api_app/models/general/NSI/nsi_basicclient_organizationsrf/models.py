from tortoise import fields, models
from MODS.standart_namespace.models import asf


class ORM_nsi_basicclient_organizationsrf(models.Model):
    """
    супер инфа
    """
    __original_dict_name__ = 'Organizations RF'
    __original_client_name__ = 'Basic client'

    
    # ИНН
    INN888 = fields.CharField(
        description ='ИНН', max_length=100, pk=True
    )
    
    # OKTMO
    OKTMO = fields.CharField(
        description ='OKTMO', max_length=100
    )
    

    class Meta:
        table = asf('nsi_basicclient_organizationsrf')
