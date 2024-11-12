from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import Student, Teacher
# , AnotherModel
from django import forms


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id', 'username', 'first_name', 'middle_name', 
        'last_name', 'email', 'phone', 'sex', 'learning_mode', 
        'payment_method', 'strand', 'tvl_specifics', 'branch',
        'created_at', 'updated_at')

    list_filter = ('sex', 'learning_mode', 'payment_method', 'strand', 'tvl_specifics', 'branch')
    search_fields = ('username', 'first_name', 'middle_name', 'last_name', 'email', 'student_id')
    ordering = ('last_name', 'first_name')
    readonly_fields = ('created_at', 'updated_at')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['payment_method'].disabled = True
        return form

    def clean_last_name(self, last_name):
        """Ensure that the last_name starts with a letter."""
        if not last_name[0].isalpha():
            raise ValidationError('Last name must start with a letter.')
        return last_name

    fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'middle_name', 'last_name', 'email', 'phone')
        }),
        ('Academic Information', {
            'fields': ('sex', 'learning_mode', 'payment_method', 'strand', 'tvl_specifics', 'branch')
        }),
        ('Emergency Contact Information', {
            'fields': (
                'emergency_contact_name',
                'emergency_contact_relationship',
                'emergency_contact_phone',
                'emergency_contact_email'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Optional: Collapse this section by default
        }),
    )

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'teacher_strand', 'created_at', 'updated_at')
    search_fields = ('user__email', 'subject')
    list_filter = ('teacher_strand', 'subject')  # Add filters for easier navigation
    ordering = ('-created_at',)  # Order by creation date descending
    fieldsets = (
        (None, {
            'fields': ('user', 'subject', 'teacher_strand', 'tvl_options')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Make this section collapsible
        }),
    )
    readonly_fields = ('created_at', 'updated_at')  # Make created_at and updated_at read-only

    def get_queryset(self, request):
        # Optionally, you can customize the queryset
        qs = super().get_queryset(request)
        return qs.select_related('user')  # Optimize query by selecting related user

    def user_email(self, obj):
        return obj.user.email if obj.user else 'No User'
    user_email.short_description = 'User  Email'  # Custom column name

# @admin.register(AnotherModel)
# class AnotherModelAdmin(admin.ModelAdmin):
#     list_display = ('teacher',)  # Only display the teacher field
#     search_fields = ('teacher__user__email', 'teacher__subject')  # Allow searching by teacher's user email and subject
#     list_filter = ('teacher__teacher_strand',)  # Filter by teacher strand if applicable
#     ordering = ('teacher',)  # Order by teacher or any other relevant field

#     fieldsets = (
#         (None, {
#             'fields': ('teacher',)  # Include the teacher field
#         }),
#     )

#     def get_queryset(self, request):
#         # Optionally, you can customize the queryset
#         qs = super().get_queryset(request)
#         return qs.select_related('teacher')  # Optimize query by selecting related teacher

#     def teacher_email(self, obj):
#         return obj.teacher.user.email if obj.teacher and obj.teacher.user else 'No User'
#     teacher_email.short_description = 'Teacher Email'  # Custom column name