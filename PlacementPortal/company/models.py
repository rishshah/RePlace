from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class Company(models.Model):
    id = models.AutoField("Company ID", primary_key=True)
    name = models.CharField("Company name", max_length=50, null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company")
    phone_number = models.CharField("Phone number", validators=[phone_regex], max_length=15, blank=True)
    category = models.ForeignKey("company.Category", verbose_name="Category", null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        permissions = (("be_company",),)

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
