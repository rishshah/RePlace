from django.db import models
from django.contrib.auth.models import User


class IC(models.Model):
    student = models.ForeignKey("student.Student", verbose_name="Student",null=False, blank=False, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="ic")

    def __str__(self):
        return "%s (IC)" % (self.student,)
    # class Meta:
    #     permissions = ("be_ic",),