from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, StreamingHttpResponse
from django.views import View
from .forms import EnrollForm, MessageForm, TeacherForm, CommunityForm, EventForm
from .models import Student, Message, Teacher, Community, Event
from django.contrib.auth.models import User

class MyAsyncView(View):
    async def get(self, request, *args, **kwargs):
        async def async_data_generator():
            for i in range(10):  # Simulating data generation
                yield f"Data chunk {i}\n"
                await asyncio.sleep(1)  # Simulate a delay
        response = StreamingHttpResponse(async_data_generator())
        response['Content-Type'] = 'text/plain'
        return response

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_500_view(request):
    return render(request, '500.html', status=500)

def logout_view(request):
    """Log the user out and redirect to the home page."""
    logout(request)
    return redirect('home')

def home(request):
    """Render home page."""
    students = Student.objects.all()  # Fetch all students
    return render(request, 'core/general/home.html', {'students': students})

def teacher_list(request):
    """Render teacher list."""
    teachers = Teacher.objects.all()  # Fetch all teachers
    return render(request, 'core/superuser/teacher_list.html', {'teachers': teachers})

def event(request):
    """View to create a new event."""
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.teacher = request.user.teacher
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event')  # Redirect to an event list or detail view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventForm()

    events = Event.objects.all()  # Fetch all events
    return render(request, 'core/school/event.html', {'form': form, 'events': events})
    
def courses(request):
    """Render courses page."""
    return render(request, 'core/school/courses.html')


def survey(request):
    """Render survey page."""
    return render(request, 'core/information/survey.html')


def contact(request):
    """Handle contact form submissions."""
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            if hasattr(request.user, 'student'):
                message.student = request.user.student
                message.save()
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('contact')
            else:
                messages.error(request, "You must be a student to send a message.")
        else:
            messages.error(request, 'There was an error in your submission. Please correct the errors below.')
    else:
        form = MessageForm()

    messages_list = Message.objects.all()  # Fetch all messages
    return render(request, 'core/school/contact.html', {'form': form, 'messages': messages_list})

def approve_message(request, message_id):
    """Approve a message."""
    message = get_object_or_404(Message, id=message_id)
    message.approved = True
    message.save()
    return redirect('contact')

def delete_message(request, message_id):
    """Delete a message."""
    message = get_object_or_404(Message, id=message_id)
    message.delete()
    messages.success(request, 'Message deleted successfully!')
    return redirect('contact')

def user_login(request):
    """Handle user login."""
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def success(request):
    """Render success page."""
    return render(request, 'core/general/success.html')

def access_denied(request):
    """Render access denied page."""
    return render(request, 'core/general/access_denied.html')

def privacy_policy(request):
    """Render privacy policy page."""
    return render(request, 'core/general/privacy_policy.html')

def terms_of_service(request):
    """Render terms of service page."""
    return render(request, 'core/general/terms_of_service.html')

def enroll(request):
    """Handle student enrollment."""
    if request.method == 'POST':
        form = EnrollForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different one.')
                return render(request, 'core/information/enroll.html', {'form': form})

            user = User.objects.create_user(
                username=username,
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            student = Student(
                user=user,
                username=user.username,
                email=user.email,
                first_name=form.cleaned_data['first_name'],
                middle_name=form.cleaned_data.get('middle_name', ''),
                last_name=form.cleaned_data['last_name'],
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone'],
                sex=form.cleaned_data['sex'],
                mother_tongue=form.cleaned_data['mother_tongue'],
                religion=form.cleaned_data['religion'],
                learning_mode=form.cleaned_data['learning_mode'],
                payment_method=form.cleaned_data['payment_method'],
                strand=form.cleaned_data['strand'],
                branch=form.cleaned_data['branch'],
                emergency_contact_name=form.cleaned_data['emergency_contact_name'],
                emergency_contact_phone=form.cleaned_data['emergency_contact_phone'],
                emergency_contact_relationship=form.cleaned_data['emergency_contact_relationship'],
                emergency_contact_email=form.cleaned_data['emergency_contact_email'],
            )

            try:
                student.save()
                messages.success(request, 'Student enrolled successfully!')
                return redirect('success')
            except Exception as e:
                messages.error(request, f'Error enrolling student: {e}')
                return render(request, 'core/information/enroll.html', {'form': form})
        else:
            messages.error(request, 'There was an error in your submission. Please correct the errors below.')
    else:
        form = EnrollForm()

    return render(request, 'core/information/enroll.html', {'form': form})

@login_required
def student_list(request):
    """Display list of students for admin users."""
    if not request.user.is_superuser:
        return redirect('access_denied')

    students = Student.objects.all()
    return render(request, 'core/teacher/student_list.html', {'students': students})

@login_required
def user_list(request):
    """Display list of users for admin users."""
    if not request.user.is_superuser:
        return redirect('access_denied')

    users = User.objects.all()
    return render(request, 'core/superuser/user_list.html', {'users': users})

@login_required
def edit_student(request, student_id):
    """Edit student information."""
    student = get_object_or_404(Student, student_id=student_id)

    if request.method == 'POST':
        form = EnrollForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student information updated successfully!')
            return redirect('student_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EnrollForm(instance=student)

    return render(request, 'core/edit-delete/edit_student.html', {'form': form, 'student': student})

@login_required
def delete_student(request, student_id):
    """Delete a student."""
    student = get_object_or_404(Student, student_id=student_id)
    student.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('student_list')

def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'core/user-interface/login.html')

@login_required
def profile(request):
    """Render user profile."""
    student = Student.objects.filter(user=request.user).first()
    teacher = Teacher.objects.filter(user=request.user).first()
    return render(request, 'core/user-interface/profile.html', {'student': student, 'teacher': teacher})

def approve_student(request, student_id):
    """Approve a student."""
    student = get_object_or_404(Student, id=student_id)
    student.is_approved = True  # Assuming you have an 'is_approved' field
    student.save()
    return redirect('student_list')

def community(request):
    """Handle community posts."""
    if request.method == 'POST':
        form = CommunityForm(request.POST, request.FILES)
        if form.is_valid():
            community_entry = form.save(commit=False)
            community_entry.teacher = request.user.teacher
            community_entry.save()
            messages.success(request, 'Your post has been submitted successfully!')
            return redirect('community')
        else:
            messages.error(request, 'There was an error in your submission. Please correct the errors below.')
    else:
        form = CommunityForm()

    community_entries = Community.objects.all()
    return render(request, 'core/school/community.html', {'community_entries': community_entries, 'form': form})

def delete_community(request, community_id):
    """Delete a community post."""
    community = get_object_or_404(Community, id=community_id)
    if request.method == 'POST':
        community.delete()
        messages.success(request, 'Community post deleted successfully!')
        return redirect('community')
    return render(request, 'core/edit-delete/delete-post.html', {'community': community})

def delete_event(request, event_id):
    """Delete a community post."""
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event post deleted successfully!')
        return redirect('event')
    return render(request, 'core/edit-delete/delete-event.html', {'event': event})

def add_subject(request):
    """Add a new subject."""
    if request.method == 'POST':
        subject_name = request.POST.get('name')
        teacher_id = request.POST.get('teacher_id')
        try:
            teacher = Teacher.objects.get(id=teacher_id)
            subject = Subject(name=subject_name)
            subject.save()
            teacher.subjects.add(subject)
            return JsonResponse({'success': True})
        except Teacher.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Teacher not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def edit_subject(request):
    """Edit a subject."""
    if request.method == 'POST':
        subject_id = request.POST.get('id')
        subject_name = request.POST.get('name')
        if not subject_id or not subject_name:
            return JsonResponse({'success': False, 'error': 'Missing subject ID or name'}, status=400)
        try:
            subject = Subject.objects.get(id=subject_id)
            subject.name = subject_name
            subject.save()
            return JsonResponse({'success': True})
        except Subject.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Subject not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def remove_subject(request):
    """Remove a subject."""
    if request.method == 'POST':
        subject_id = request.POST.get('id')
        if not subject_id:
            return JsonResponse({'success': False, 'error': 'Missing subject ID'}, status=400)
        try:
            subject = Subject.objects.get(id=subject_id)
            subject.delete()
            return JsonResponse({'success': True})
        except Subject.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Subject not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def stem_view(request):
    """Render STEM strand page."""
    return render(request, 'core/strands/stem.html')

def abm_view(request):
    """Render ABM strand page."""
    return render(request, 'core/strands/abm.html')

def humss_view(request):
    """Render HUMSS strand page."""
    return render(request, 'core/strands/humss.html')

def gas_view(request):
    """Render GAS strand page."""
    return render(request, 'core/strands/gas.html')

def tvl_view(request):
    """Render TVL strand page."""
    return render(request, 'core/strands/tvl.html')

def la_forteza(request):
    """Render La Forteza branch page."""
    return render(request, 'branch/la_forteza.html')

def login_branch(request):
    """Render login page for branch."""
    return render(request, 'branch/login_branch.html')

def dashboard(request):
    """Render teacher dashboard."""
    students = Student.objects.all()
    return render(request, 'core/teacher/dashboard.html', {'students': students})

def grading(request, student_id):
    """Render grading page for a specific student."""
    student = Student.objects.get(id=student_id)
    return render(request, 'core/teacher/grading.html', {'student': student})

def subject(request):
    """Render subject page."""
    return render(request, 'core/teacher/subject.html')

def lesson(request):
    """Render lesson page."""
    return render(request, 'core/teacher/lesson.html')

def add_login_teacher(request):
    """Render add login teacher page."""
    return render(request, 'core/teacher/teacher.html')

def teacher_register(request):
    """Handle teacher registration."""
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher registered successfully!')
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'core/superuser/teacher.html', {'form': form})

def update_teacher(request, teacher_id):
    """Update teacher information."""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher updated successfully!')
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'core/superuser/teacher_list.html', {'form': form})