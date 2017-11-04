from django.contrib import admin
from .models import Department, Program, Student, Application, Resume

# Register your models here.
admin.site.register(Department)
admin.site.register(Program)
admin.site.register(Student)
admin.site.register(Application)
admin.site.register(Resume)