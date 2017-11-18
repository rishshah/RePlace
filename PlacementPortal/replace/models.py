from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator, MinLengthValidator
from django.contrib.auth.models import User
# Create your models here.
class Application(models.Model):
    student = models.ForeignKey("student.Student", verbose_name="Applicant", null=False, blank=False, on_delete=models.CASCADE)
    jaf = models.ForeignKey("company.JAF", verbose_name="Job application", null=False, blank=False, on_delete=models.CASCADE)
    review = models.TextField("Job review", null=True, blank=True)
    is_selected = models.BooleanField("Selected?", null=False, blank=False, default=False)
    progress = models.IntegerField("Number of tests passed", null=False, blank=False, default=0)

    def __str__(self):
        return "%s's application for %s"%(self.student, self.jaf)

    class Meta:
        unique_together = (("student", "jaf"),)