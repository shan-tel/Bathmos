from django.contrib import admin
from .models import ClassName, Student, Subject, Teacher, Score

admin.site.register(ClassName)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Score)
# Register your models here.
