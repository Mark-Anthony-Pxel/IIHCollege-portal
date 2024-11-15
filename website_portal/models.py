from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import uuid
from datetime import date

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    student_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    username = models.CharField(max_length=20, unique=True, verbose_name=_('Username'))
    first_name = models.CharField(max_length=20, verbose_name=_('First Name'))
    middle_name = models.CharField(max_length=20, blank=True, verbose_name=_('Middle Name'))
    last_name = models.CharField(max_length=20, verbose_name=_('Last Name'))
    address = models.CharField(max_length=100, verbose_name=_('Address'))
    phone = models.CharField(max_length=13, verbose_name=_('Phone Number'))
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    password = models.CharField(max_length=128, verbose_name=_('Password'))  # Store hashed password
        # Emergency contact fields 'optional'
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, null=True, blank=True)
    emergency_contact_email = models.EmailField(null=True, blank=True)


    SEX_CHOICES = [
        ('Male', _('Male')),
        ('Female', _('Female')),
        ('Other', _('Other')),
    ]
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, verbose_name=_('Sex'))
    mother_tongue = models.CharField(max_length=30, verbose_name=_('Mother Tongue'))
    religion = models.CharField(max_length=30, verbose_name=_('Religion'))
    
    LEARNING_MODE_CHOICES = [
        ('Modular', _('Modular')),
        ('Face to face', _('Face to Face')),
        ('Online', _('Online')),
        ('Hybrid', _('Hybrid')),
    ]
    learning_mode = models.CharField(max_length=15, choices=LEARNING_MODE_CHOICES, verbose_name=_('Learning Mode'))
    
    PAYMENT_METHOD_CHOICES = [
        ('Cash', _('Cash')),
        ('Bank Transfer', _('Bank Transfer')),
        ('Mobile Wallet', _('Mobile Wallet')),
    ]
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHOD_CHOICES, verbose_name=_('Payment Method'))
    
    STRAND_CHOICES = [
        ('STEM', _('STEM')),
        ('ABM', _('ABM')),
        ('HUMSS', _('HUMSS')),
        ('GAS', _('GAS')),
        ('TVL', _('TVL')),
    ]
    strand = models.CharField(max_length=5, choices=STRAND_CHOICES, verbose_name=_('Strand'))

    TVL_SPECIFICS = [
        ('HE - Cookery', _('HE - Cookery')),
        ('HE - Tourism', _('HE - Tourism')),
        ('ICT', _('ICT')),
    ]    
    tvl_specifics = models.CharField(max_length=15, choices=TVL_SPECIFICS, blank=True, null=True, verbose_name=('Specifics'))

    BRANCH_CHOICES = [
        ('La Forteza Campus', _('IIH COLLEGE - La Forteza Campus')),
        ('Zabarte Fairview Campus', _('IIH COLLEGE - Zabarte Fairview Campus')),
        ('Novaliches Campus', _('IIH COLLEGE - Novaliches Campus')),
        ('Brixton Camarin Campus', _('IIH COLLEGE - Brixton Camarin Campus')),
        # Add more branches as needed
    ]
    branch = models.CharField(max_length=50, choices=BRANCH_CHOICES, verbose_name=_('Branch'))

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name} ({self.username})"

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)  # Hash the password
        if not self.user_id:  # Check if user_id is not set
            raise ValueError("User  must be assigned before saving the Student instance.")
        super().save(*args, **kwargs)
  
class Message(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Optional fields
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True, verbose_name=_('Attachment'))
    is_read = models.BooleanField(default=False, verbose_name=_('Is Read'))
    
    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __str__(self):
        return f"Message from {self.student} - {self.subject or 'No Subject'}"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher', null=True, blank=True)
    subject = models.CharField(max_length=50)
    password = models.CharField(max_length=128, blank=True)  # Store hashed password
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name=_('Email'))
    first_name = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Last Name'))

    STRANDS = [
        ('STEM', _('STEM')),
        ('ABM', _('ABM')),
        ('HUMSS', _('HUMSS')),
        ('GAS', _('GAS')),
        ('TVL', _('TVL')),
    ]
    teacher_strand = models.CharField(max_length=5, choices=STRANDS, verbose_name=_('Teacher Strand'))

    TVL_OPTIONS = [
        ('HE - Cookery', _('HE - Cookery')),
        ('HE - Tourism', _('HE - Tourism')),
        ('ICT', _('ICT')),
    ]    
    tvl_options = models.CharField(max_length=15, choices=TVL_OPTIONS, blank=True, null=True, verbose_name=_('Teacher TVL'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)  # Hash the password
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Teacher')
        verbose_name_plural = _('Teachers')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.subject}"

from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name