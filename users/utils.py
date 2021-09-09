from django.core.exceptions import ValidationError

def _phone_validation(value):
    if value[0]!='+':
        raise ValidationError(f'номер {value} веден неправильно. Формат вода +79999999999')

def _create_path_media_user(instance, filename):
    return f'Пользователи/{instance.position}/{instance.full_name}/Профиль_{instance.last_name}_.{filename.split(".")[-1]}'
