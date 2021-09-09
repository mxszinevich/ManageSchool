from django.contrib import admin
from .models import  StaffUser, Student,User,ParentsStudent

admin.site.register(StaffUser)
admin.site.register(Student)
admin.site.register(User)
admin.site.register(ParentsStudent)
