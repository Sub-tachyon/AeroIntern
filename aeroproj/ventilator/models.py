from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    patient_id = models.CharField(max_length=50, unique=True)
    age = models.IntegerField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    STATUS_CHOICES = [
        ('PASSIVE', 'Passive'),
        ('EMERGENCY', 'Emergency'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PASSIVE')

class Ventilator(models.Model):
    #email = models.CharField(max_length=255,null=True)
    serial_number = models.CharField(max_length=50, unique=True)
    #is_available = models.BooleanField(default=True)
    #assigned_to = models.CharField(max_length=100, null=True, blank=True)   
    location = models.CharField(max_length=100, null=True, blank=True) 
    model = models.CharField(max_length=100, null=True, blank=True)  

