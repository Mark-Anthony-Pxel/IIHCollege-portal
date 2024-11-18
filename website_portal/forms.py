from django import forms
from django.core.validators import validate_email, RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Student, Message, Teacher, Community, Event
from django.contrib.auth.models import User

class EnrollForm(forms.ModelForm):

    # Student Information
    username = forms.CharField(
        max_length=20, 
        label=_('Username'), 
        required=True, 
        help_text=_('Enter a unique username.')
    )
    first_name = forms.CharField(
        max_length=20, 
        label=_('First Name'), 
        required=True
    )
    middle_name = forms.CharField(
        max_length=20, 
        label=_('Middle Name'), 
        required=False
    )
    last_name = forms.CharField(
        max_length=20, 
        label=_('last_name'), 
        required=True
    )
    address = forms.CharField(
        max_length=100, 
        label=_('Address'), 
        required=True, 
        help_text=_('Enter your complete address.')
    )
    
    # Phone Number Validator for Philippine Numbers
    phone_validator = RegexValidator(
        regex=r'^(09\d{9})$',  # Matches '09XXXXXXXXXX'
        message=_('Phone number must be in the format: "09XXXXXXXXXX" (11 digits total).')
    )

    phone = forms.CharField(
        max_length=11,
        label=_('Phone Number'),
        required=True,
        validators=[phone_validator],
        help_text=_('Enter your phone number in the format: "09XXXXXXXXXX" (11 digits total).')
    )
    
    email = forms.EmailField(
        label=_('Email'), 
        validators=[validate_email],
        help_text=_('Enter a valid email address.')
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput, 
        label=_('Password'),
        help_text=_('Password must be at least 8 characters long and contain a digit, an uppercase letter, and a special character.')
    )
    
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, 
        label=_('Confirm Password'),
        help_text=_('Re-enter your password for confirmation.')
    )

    sex = forms.ChoiceField(
        choices=[
            ('Male', _('Male')),
            ('Female', _('Female')),
            ('Other', _('Other')),
        ], 
        label=_('Sex'), 
        required=True
    )
    mother_tongue = forms.CharField(
        max_length=30, 
        label=_('Mother Tongue'), 
        required=True
    )
    religion = forms.CharField(
        max_length=30, 
        label=_('Religion'), 
        required=True
    )
    # Learning Mode
    learning_mode = forms.ChoiceField(
        choices=[
            ('Modular', _('Modular')),
            ('Face to face', _('Face to Face')),
            ('Online', _('Online')),
            ('Hybrid', _('Hybrid')),
        ], 
        label=_('Learning Mode')
    )
    # Payment Information
    payment_method = forms.ChoiceField(
        choices=[
            ('Cash', _('Cash')),
            ('Bank Transfer', _('Bank Transfer')),
            ('Mobile Wallet', _('Mobile Wallet')),
        ], 
        label=_('Payment Method')
    )
    # Additional Information
    strand = forms.ChoiceField(
        choices=[
            ('STEM', _('STEM')),
            ('ABM', _('ABM')),
            ('HUMSS', _('HUMSS')),
            ('GAS', _('GAS')),
            ('TVL', _('TVL')),
        ], 
        label=_('Strand')
    )
    tvl_specifics = forms.ChoiceField(
        choices=[
            ('HE - Cookery', _('HE - Cookery')),
            ('HE - Tourism', _('HE - Tourism')),
            ('ICT', _('ICT')),
        ], 
        label=_('Specifics'),
        required=False 
    )
    branch = forms.ChoiceField(
        choices=[
            ('La Forteza Campus', _('IIH COLLEGE - La Forteza Campus')),
            ('Zabarte Fairview Campus', _('IIH COLLEGE - Zabarte Fairview Campus')),
            ('Novaliches Campus', _('IIH COLLEGE - Novaliches Campus')),
            ('Brixton Camarin Campus', _('IIH COLLEGE - Brixton Camarin Campus')),
            # Add more branches as needed
        ], 
        label=_('Branch'), 
        required=True
    )
    # Emergency Contact Information
    emergency_contact_name = forms.CharField(
        max_length=50, 
        label=_('Emergency Contact Name'), 
        required=True
    )
    emergency_contact_relationship = forms.CharField(
        max_length=20, 
        label=_('Emergency Contact Relationship'), 
        required=True
    )
    emergency_contact_phone = forms.CharField(
        max_length=11, 
        label=_('Emergency Contact Phone'), 
        required=True, 
        validators=[phone_validator],
        help_text=_('Enter the emergency contact phone number starting with "09".')
    )
    emergency_contact_email = forms.EmailField(
        label=_('Emergency Contact Email'), 
        validators=[validate_email],
        required=False,
        help_text=_('Enter a valid email address for the emergency contact.')
    )

    class Meta:
        model = Student
        fields = [
            'username', 'first_name', 'middle_name', 'last_name', 
            'email', 'phone', 'address', 'sex', 'mother_tongue', 'religion', 
            'learning_mode', 'payment_method', 
            'strand', 'tvl_specifics', 'branch', 'password', 'password_confirm',
            'emergency_contact_name', 'emergency_contact_relationship', 
            'emergency_contact_phone', 'emergency_contact_email'
        ]
        widgets = {
            'password': forms.PasswordInput(),
            'password_confirm': forms.PasswordInput()
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if Student.objects.filter(username=username).exists():
            raise ValidationError(_('This username is already taken. Please choose another one.'))
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@gmail.com'):  # Update this to allow multiple domains
            raise ValidationError(_('Please use a valid Google email address.'))
        if Student.objects.filter(email=email).exists():
            raise ValidationError(_('This email is already registered. Please use another one.'))
        return email

    def clean_address(self):
        address = self.cleaned_data['address']
        if not address.strip():
            raise ValidationError(_('Address cannot be empty. Please provide a valid address.'))
        return address

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError(_('Password must be at least 8 characters long.'))
        return password

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError(_('Passwords do not match. Please try again.'))
        return password_confirm

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        return self.validate_phone_number(phone)

    def validate_phone_number(self, phone):
        if not phone.startswith('09'):
            raise ValidationError(_('Phone number must start with "09"'))
        return phone

    def clean_emergency_contact_phone(self):
        
        emergency_contact_phone = self.cleaned_data['emergency_contact_phone']
        return self.validate_phone_number(emergency_contact_phone)

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message', 'attachment', 'image']
        labels = {
            'image': 'Image (optional)',
            'message': 'Message',
            'attachment': 'Attachment (optional)',
        }
        help_texts = {
            'image': 'Upload an image (optional, max 5MB).',
            'attachment': 'Upload an optional file (max 10MB).',
        }

class TeacherForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Teacher
        fields = ['subject', 'teacher_strand', 'tvl_options']  # Exclude user fields

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        # Create the User instance
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            is_staff=True,
            is_superuser=False
        )
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()  # Save the User instance

        # Create the Teacher instance
        teacher = super().save(commit=False)
        teacher.user = user  # Associate the User with the Teacher
        if commit:
            teacher.save()  # Save the Teacher instance
        return teacher

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['comment', 'image', 'attachment']
        labels = {
            'comment': 'Comment',
            'image': 'Image',
            'attachment': 'Attachment',
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title','teacher', 'event_post', 'visibility', 'image', 'attachment']
        help_texts = {
            'title': 'Enter your title here',
            'event_post': 'Enter your event description here.',
            'visibility': 'Select the visibility of the event.',
            'image': 'Upload an event image.',
            'attachment': 'Upload an optional file.',
        }