from django.urls import path
from . import views
from .views import (
    login_view, logout_view,
    delete_student, approve_student, approve_message, delete_message,
    teacher_register, edit_subject, add_subject, remove_subject,
    community, stem_view, abm_view, humss_view, gas_view, tvl_view,
    contact, dashboard, event
)

urlpatterns = [
    # Home and General Views
    path('', views.home, name='home'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('access-denied/', views.access_denied, name='access_denied'),
    path('student/of/iihc/', views.survey, name='survey'),

    # User Management
    path('users/', views.user_list, name='user_list'),
    path('login/', login_view, name='login'),  # Updated to use login_view
    path('logout/', logout_view, name='logout'),

    # Student Management
    path('enroll/', views.enroll, name='enroll'),
    path('students/', views.student_list, name='student_list'),
    path('profile/', views.profile, name='profile'),
    path('approve-student/<uuid:student_id>/', approve_student, name='approve_student'),
    path('delete-student/<uuid:student_id>/', delete_student, name='delete_student'),

    # Additional Pages
    path('courses/', views.courses, name='courses'),
    path('event/', event, name='event'),
    path('community/', community, name='community'),
    path('contact/', contact, name='contact'),

    # Teacher Pages
    path('teacher/dashboard/', dashboard, name='dashboard'),
    path('teacher/grading/<uuid:student_id>/', views.grading, name='grading'),  # Added student_id as a parameter
    path('teacher/subject/', views.subject, name='subject'),
    path('teacher/lesson/', views.lesson, name='lesson'),
    path('login/branch/', views.login_branch, name='login_branch'),

    # Branch Page
    path('la_forteza/', views.la_forteza, name='la_forteza'),

    # Strand Pages
    path('strand/stem/', stem_view, name='stem_strand'),
    path('strand/abm/', abm_view, name='abm_strand'),
    path('strand/humss/', humss_view, name='humss_strand'),
    path('strand/gas/', gas_view, name='gas_strand'),
    path('strand/tvl/', tvl_view, name='tvl_strand'),

    # Success Page
    path('success/', views.success, name='success'),

    # Message Management
    path('approve-message/<int:message_id>/', approve_message, name='approve_message'),
    path('delete-message/<int:message_id>/', delete_message, name='delete_message'),

    # Admin Pages
    path('teacher/admin/register/', teacher_register, name='teacher_register'),
    path('teacher/admin/list/', views.teacher_list, name='teacher_list'),

    # Subject Management
    path('admin/add-subject/', add_subject, name='add_subject'),
    path('admin/edit-subject/', edit_subject, name='edit_subject'),
    path('admin/remove-subject/', remove_subject, name='remove_subject'),

    # Community Management
    path('community/delete/<int:community_id>/', views.delete_community, name='delete_community'),

    # Async Data
    path('async-data/', views.MyAsyncView.as_view(), name='async_data'),

    # Password Reset (commented out for future implementation)
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uuid:student_id>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]