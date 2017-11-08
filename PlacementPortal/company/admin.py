from django.contrib import admin
from .models import Company, Category, JAF, JAFTest, TestType, Eligibility

admin.site.register(Company)
admin.site.register(Category)
admin.site.register(JAF)
admin.site.register(JAFTest)
admin.site.register(TestType)
admin.site.register(Eligibility)
# Register your models here.
