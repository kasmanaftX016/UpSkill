from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView, DetailView
from .models import Subject, Course ,User
from .utils import send_verification_code
from django.utils import timezone
from datetime import timedelta



def index(request):
    return render(request, 'upskill/index.html')


class SubjectListView(ListView):
    model = Subject
    template_name = 'upskill/subject_list.html'
    context_object_name = 'subjects'


class CourseListBySubjectView(ListView):
    model = Course
    template_name = 'upskill/course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        self.subject = get_object_or_404(Subject, slug=self.kwargs['slug'])
        return Course.objects.filter(subject=self.subject)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = self.subject
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'upskill/course.html'
    context_object_name = 'course'


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
    return render(request, "upskill/register.html")


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            is_active=False
        )

        send_verification_code(user)
        request.session['email'] = email
        return redirect('verify')

    return render(request, 'register.html')



def verify(request):
    error = None

    if request.method == 'POST':
        code = request.POST['code']
        email = request.session.get('email')

        user = User.objects.get(email=email)

       
        if timezone.now() > user.code_created_at + timedelta(minutes=1):
            error = "Kod vaqti tugagan. Qayta yuboring."
        elif user.email_code == code:
            user.is_active = True
            user.is_email_verified = True
            user.email_code = ''
            user.save()
            return redirect('login')
        else:
            error = "Kod notogri"

    return render(request, 'verfiy.html', {'error': error})


def resend_code(request):
    email = request.session.get('email')
    user = User.objects.get(email=email)

    send_verification_code(user)
    return redirect('verify')
