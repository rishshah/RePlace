from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class Student:
    id = models.AutoField("Student ID", primary_key=True)
    name = models.CharField("Full name", max_length=50, null=False, blank=False)
    email = models.EmailField("Email ID", null=False, blank=False)
    phone = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    reg_year = models.IntegerField(validators=[MinValueValidator(1958), MaxValueValidator(2018)], null=False, blank = False)
    cpi = models.FloatField(validators=[MinValueValidator(0.0),MaxValueValidator(10.0)])
    ldap_id = models.CharField("LDAP ID", validators=[MinLengthValidator(9), MaxValueValidator(9)])
    ldap_password = models.CharField("LDAP password", max_length=100, validators=[MinLengthValidator(8)])
    department = models.ForeignKey()
