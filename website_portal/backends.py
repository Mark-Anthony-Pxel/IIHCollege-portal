# backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
# from .models import Teacher

User  = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

# class TeacherBackend(BaseBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         try:
#             teacher = Teacher.objects.get(email=email)
#             if teacher.check_password(password):
#                 return teacher
#         except Teacher.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return Teacher.objects.get(pk=user_id)
#         except Teacher.DoesNotExist:
#             return None