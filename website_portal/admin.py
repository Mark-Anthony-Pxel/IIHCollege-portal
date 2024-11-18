from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Student, Teacher, Message, Community, Event

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id', 'username', 'first_name', 'middle_name', 
        'last_name', 'email', 'phone', 'sex', 'learning_mode', 
        'payment_method', 'strand', 'tvl_specifics', 'branch',
        'created_at', 'updated_at'
    )

    list_filter = ('sex', 'learning_mode', 'payment_method', 'strand', 'tvl_specifics', 'branch')
    search_fields = ('username', 'first_name', 'middle_name', 'last_name', 'email', 'student_id')
    ordering = ('last_name', 'first_name')
    readonly_fields = ('created_at', 'updated_at')

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

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'teacher_strand', 'created_at', 'updated_at')
    search_fields = ('user__email', 'subject')
    list_filter = ('teacher_strand', 'subject')  # Add filters for easier navigation
    ordering = ('-created_at',)  # Order by creation date descending
    readonly_fields = ('created_at', 'updated_at')  # Make created_at and updated_at read-only

    fieldsets = (
        (None, {
            'fields': ('user', 'subject', 'teacher_strand', 'tvl_options')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Make this section collapsible
        }),
    )

    def get_queryset(self, request):
        # Optionally, you can customize the queryset
        qs = super().get_queryset(request)
        return qs.select_related('user')  # Optimize query by selecting related user

    def user_email(self, obj):
        return obj.user.email if obj.user else 'No User'
    user_email.short_description = 'User  Email'  # Custom column name

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('student', 'message', 'approved', 'is_read', 'created_at')
    search_fields = ('student__username', 'message')
    list_filter = ('approved', 'is_read', 'created_at')
    ordering = ('-created_at',)  # Order by creation date descending
    readonly_fields = ('created_at',)  # Make created_at read-only

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'post', 'visibility', 'created_at', 'updated_at')
    search_fields = ('teacher__user__username', 'post')
    list_filter = ('visibility', 'created_at')
    ordering = ('-created_at',)  # Order by creation date descending
    readonly_fields = ('created_at', 'updated_at')  # Make created_at and updated_at read-only

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'title', 'event_post', 'visibility', 'created_at', 'updated_at')
    search_fields = ('teacher__user__username', 'title', 'event_post')
    list_filter = ('visibility', 'created_at')
    ordering = ('-created_at',)  # Order by creation date descending
    readonly_fields = ('created_at', 'updated_at')  # Make created_at and updated_at read-only
