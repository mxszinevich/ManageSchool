from rest_framework import serializers
from users.models import StaffUser
import  pprint
class StaffUserSerializer(serializers.ModelSerializer):
    # @TODO добавить проверку пароля

    class Meta:
        model=StaffUser
        fields = (
            'id','first_name','last_name',
            'middle_name','email','image',
            'date_of_birth', 'phone_number','position'
        )
        read_only = ('password',)

    def save(self, **kwargs):

        staff_user=StaffUser(**self.validated_data)
        staff_user.set_password(self.validated_data['password'])
        staff_user.save()

        return staff_user




