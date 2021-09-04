from django.core.exceptions import ValidationError

def _phone_validation(value):
    if value[0]!='+':
        raise ValidationError(f'номер {value} веден неправильно. Формат вода +79999999999')