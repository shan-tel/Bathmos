from django.contrib import admin
from .models import ClassName, Student, Subject, Teacher

admin.site.register(ClassName)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Teacher)
# Register your models here.
