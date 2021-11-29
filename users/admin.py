from django.contrib import admin
from .models import StaffUser, Student,User,ParentsStudent

class GroupStudent(admin.ModelAdmin):
	list_filter = ('educational_class',)

admin.site.register(StaffUser)
admin.site.register(Student, GroupStudent)
admin.site.register(User)
admin.site.register(ParentsStudent)


