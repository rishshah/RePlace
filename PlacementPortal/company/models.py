from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator, MaxLengthValidator, MinLengthValidator

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class Company(models.Model):
    id = models.AutoField("Company ID", primary_key=True)
    name = models.CharField("Company name", max_length=50, null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company")
    phone_number = models.CharField("Phone number", validators=[phone_regex], max_length=15, blank=True)
    category = models.ForeignKey("company.Category", verbose_name="Category", null=False, blank=False, on_delete=models.CASCADE)

    # class Meta:
    #     permissions = ("be_company",)

class Category(models.Model):
    type = models.CharField(max_length=30, primary_key=True, blank=False)

class JAF(models.Model):
    id = models.AutoField("JAF no.", primary_key=True)
    company = models.ForeignKey("company.Company", verbose_name="Company", null=False, blank=False, on_delete=models.CASCADE)
    description = models.TextField("Job description", null=False, blank=False)
    other_details = models.TextField("Other details", null=True, blank=True)
    requirements = models.TextField("Job requirements", null=False, blank=False)
    job_year = models.IntegerField("Registration year", validators=[MinValueValidator(1958), MaxValueValidator(2018)], null=False, blank = False)
    posting = models.CharField("Place of posting", max_length=50, null=False, blank=False)
    profile = models.CharField("Job profile", max_length=50, null=False, blank=False)
    accomodation = models.TextField("Accomodation details", null=False, blank=False)
    duration = models.IntegerField("Internship duration (days)", validators=[MinValueValidator(7)], null=False, blank=False)
    resume_number = models.IntegerField("Resume no. wanted", validators=[MinValueValidator(0), MaxValueValidator(3)], null=True, blank=True)

class JAFTest(models.Model):
    jaf = models.ForeignKey("company.JAF", verbose_name="JAF", null=False, blank=False, on_delete=models.CASCADE)
    test_number = models.IntegerField("Test no.", null=False, blank=False)
    location = models.CharField("Test venue/URL", max_length=50, null=True, blank=True)
    start_time = models.DateTimeField("Test time", null=True, blank=True)
    description = models.TextField("Test details", null=True, blank=True)
    test_type = models.ForeignKey("TestType", verbose_name="Test type", null=False, blank=False, on_delete=models.CASCADE)
    duration = models.FloatField("Test duration (minutes)")

    class Meta:
        unique_together = (("test_number", "jaf"),)


class TestType(models.Model):
    type = models.CharField("Test type", max_length=50, primary_key=True)

class Eligibility(models.Model):
    jaf = models.ForeignKey("JAF", verbose_name="JAF", null=False, blank=False, on_delete=models.CASCADE)
    department = models.ForeignKey("student.Department", verbose_name="Department", null=False, blank=False, on_delete=models.CASCADE)
    program = models.ForeignKey("student.Program", verbose_name="Program", null=False, blank=False, on_delete=models.CASCADE)
    cpi_cutoff = models.FloatField("CPI", validators=[MinValueValidator(0.0),MaxValueValidator(10.0)], null=False, blank=False)
    stipend = models.DecimalField("Compensation", decimal_places=2, max_digits=10, null=False, blank=False)
    currency = models.CharField("Unit",validators=[MinLengthValidator(3), MaxLengthValidator(3)], max_length=3, null=False, blank=False)

    class Meta:
        unique_together = (("department", "jaf", "program"),)
