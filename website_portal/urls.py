from django.urls import path
from . import views
# Importing views related to authentication
from .views import login, logout_view

# Importing views related to student management
from .views import delete_student, approve_student, approve_message, delete_message

# Importing views related to subjects and teachers
from .views import teacher_register, edit_subject, add_subject, remove_subject

# Importing views related to specific strands
from .views import stem_view, abm_view, humss_view, gas_view, tvl_view

# Importing other views
from .views import contact, dashboard

#URL path
from .views import MyAsyncView


urlpatterns = [
    # Home and General Views
    path('', views.home, name='home'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('access-denied/', views.access_denied, name='access_denied'),
    # path('error/', views.error, name='error'),

    # User Management
    path('users/', views.user_list, name='user_list'),
    path('login/', login, name='login'),
    # path('register/', views.register, name='register'),
    path('logout/', logout_view, name='logout'),

    # Student Management
    path('enroll/', views.enroll, name='enroll'),
    path('students/', views.student_list, name='student_list'),
    path('profile/', views.profile, name='profile'), 
    path('approve-student/<uuid:student_id>/', approve_student, name='approve_student'),  # Fixed path
    path('delete-student/<uuid:student_id>/', delete_student, name='delete_student'),  # Fixed path

    # Additional Pages
    path('courses/', views.courses, name='courses'),
    path('event/', views.event, name='event'),
    path('community/', views.community, name='community'),
    path('contact/', contact, name='contact'),

    # Teacher Pages
    path('login/branch', views.login_branch, name='login_branch'),
    path('teacher/dashboard', dashboard, name='dashboard'),
    path('teacher/grading', views.grading, name='grading'),
    path('teacher/subject', views.subject, name='subject'),
    path('teacher/lesson', views.lesson, name='lesson'),


    #Branch Page
    path('la_forteza/', views.la_forteza, name='la_forteza'),


    #strand Pages
    path('stem/', stem_view, name='stem_strand'),
    path('abm/', abm_view, name='abm_strand'),
    path('humss/', humss_view, name='humss_strand'),
    path('gas/', gas_view, name='gas_str and'),
    path('tvl/', tvl_view, name='tvl_strand'),

    # Success Page
    path('success/', views.success, name='success'),

    # contact
    path('approve-message/<int:message_id>/', approve_message, name='approve_message'),
    path('delete-message/<int:message_id>/', delete_message, name='delete_message'),  # Add this line

    #Admin Page
    path('teacher/admin/register', teacher_register, name='teacher'),
    path('teacher/admin/list', views.teacher_list, name='teacher_list'),
    path('add_subject/', add_subject, name='add_subject'),
    path('edit_subject/', edit_subject, name='edit_subject'),
    path('remove_subject/', remove_subject, name='remove_subject'),

    # URL path
    path('async-data/', MyAsyncView.as_view(), name='async_data'),  


    #Soon
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uuid:student_id>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
