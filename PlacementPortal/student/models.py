from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator, MinLengthValidator
from django.contrib.auth.models import User

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class Department(models.Model):
    name = models.CharField(max_length=30, primary_key=True, blank=False)

    def __str__(self):
        return self.name

class Program(models.Model):
    name = models.CharField(max_length=50, primary_key=True, blank=False)
    
    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    id = models.AutoField("Student ID", primary_key=True)
    name = models.CharField("Full name", max_length=50, null=False, blank=False)
    roll_number = models.CharField("Roll number", max_length=4, validators=[MinLengthValidator(4)], unique=True, null=False, blank=False)
    email = models.EmailField("Email ID", null=False, blank=False)
    phone_number = models.CharField("Phone number", validators=[phone_regex], max_length=15, blank=True)
    reg_year = models.IntegerField("Registration year", validators=[MinValueValidator(1958), MaxValueValidator(2050)], null=False, blank = False)
    cpi = models.FloatField("CPI", validators=[MinValueValidator(0.0),MaxValueValidator(10.0)], null=False, blank=False)
    resume_verified = models.BooleanField("Resume verified?", default=False, null=False, blank=False)
    department = models.ForeignKey("student.Department", verbose_name="Department", null=False, blank=False, on_delete=models.CASCADE)
    program = models.ForeignKey("student.Program", verbose_name="Program", null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Resume(models.Model):
    student = models.ForeignKey("student.Student", verbose_name="Resume of", null=False, blank=False, on_delete=models.CASCADE)
    resume_number = models.IntegerField("Resume number", choices=(
        (0,"One page"),
        (1, "Two page Tech"),
        (2, "One page Nontech"),
        (3, "CV"),
    ), null=False, blank=False)
    file = models.FileField("Resume pdf", null=False, blank=False)


    def __str__(self):
        return "%s's resume no. %d" % (self.student, self.resume_number)

    class Meta:
        unique_together = (("student", "resume_number"),)
