from django.contrib import admin
from .models import Admin,Student,Teacher,Subject,SubjectScore,StdClass,Session

admin.site.register(Admin)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(SubjectScore)
admin.site.register(Session)
from django.contrib import admin

class StdClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_students')

    def display_students(self, obj):
        students = obj.get_students()
        return ", ".join([str(student) for student in students])

    display_students.short_description = 'Students'

admin.site.register(StdClass, StdClassAdmin)



# Register your models here.
