from tortoise import fields, models
from MODS.standart_namespace.models import asf


class ORM_nsi_farmerpassport_organizations(models.Model):
    """
    Организации
    """
    __original_dict_name__ = 'organizations'
    __original_client_name__ = 'Farmer passport'

    
    # Идентификатор организации
    INN = fields.CharField(
        description ='Идентификатор организации', max_length=255, pk=True
    )
    
    # Субъект Российской Федерации
    subject = fields.CharField(
        description ='Субъект Российской Федерации', max_length=255
    )
    
    # ОКТМО
    OKTMO = fields.CharField(
        description ='ОКТМО', max_length=255
    )
    
    # Контакты
    contacts = fields.TextField(
        description ='Контакты'
    )
    
    # Дата регистрации КФХ
    KFH_registration_data = fields.DatetimeField(
        description ='Дата регистрации КФХ'
    )
    
    # Адрес регистрации
    KFH_registration_address = fields.TextField(
        description ='Адрес регистрации'
    )
    
    # ФИО главы КФХ
    KFH_full_name = fields.TextField(
        description ='ФИО главы КФХ'
    )
    
    # Возраст главы КФХ
    KFH_general_old = fields.CharField(
        description ='Возраст главы КФХ', max_length=255
    )
    
    # Наименование грантополучателя
    grant_name = fields.TextField(
        description ='Наименование грантополучателя'
    )
    
    # Вид гранта
    grant_type = fields.CharField(
        description ='Вид гранта', max_length=255
    )
    
    # Год получения гранта
    grant_year = fields.CharField(
        description ='Год получения гранта', max_length=255
    )
    
    # Размер  полученного гранта, рублей
    grant_size = fields.FloatField(
        description ='Размер  полученного гранта, рублей'
    )
    
    # Объем собственных средств грантополучателя
    grant_amount_own_funds = fields.FloatField(
        description ='Объем собственных средств грантополучателя'
    )
    
    #  в том числе заемные
    grant_amount_borrowed_funds = fields.FloatField(
        description =' в том числе заемные'
    )
    
    # Основной ОКВЭД КФХ
    grant_OKWED_KFH = fields.CharField(
        description ='Основной ОКВЭД КФХ', max_length=255
    )
    
    # Вид деятельности по ОКВЭД, на который получен грант
    grant_OKWED_type = fields.CharField(
        description ='Вид деятельности по ОКВЭД, на который получен грант', max_length=255
    )
    
    # Стоимость проекта, представленного на конкурсный отбор
    grant_project_cost = fields.FloatField(
        description ='Стоимость проекта, представленного на конкурсный отбор'
    )
    

    class Meta:
        table = asf('nsi_farmerpassport_organizations')
