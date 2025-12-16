from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Subject, Course


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
