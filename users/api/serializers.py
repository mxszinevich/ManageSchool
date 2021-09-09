from rest_framework import serializers
from users.models import StaffUser,User
from school_structure.api.serializers import SchoolSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = (
            'id','first_name','last_name',
            'middle_name','email','image',
            'date_of_birth', 'phone_number')
        read_only = ('password',)

class StaffUserSerializer(serializers.ModelSerializer):
    base_info=UserSerializer(source='user')
    school=SchoolSerializer()
    class Meta:
        model=StaffUser
        fields = ('base_info','school')


    def save(self, **kwargs):
        print(self.validated_data)
        """
        staff_user=StaffUser(**self.validated_data)
        staff_user.set_password(self.validated_data['password'])
        staff_user.save()

        return staff_user
        """




