from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


class IC(models.Model):
    student = models.ForeignKey("Student", verbose_name="Student",null=False, blank=False, on_delete=models.CASCADE)
    # ic_password = models.CharField("IC password", null=False, blank=False, validators=MinLengthValidator(8))
    # ic_email = models.EmailField("IC Email Id", null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="object")

    class Meta:
        permissions = (("be_ic",),)