from django.urls import path
from .views import (
    index,
    SubjectListView,
    CourseListBySubjectView,
    CourseDetailView,
    login_view,
    register, 
    verify, 
    resend_code

)

urlpatterns = [
    path('', index, name='index'),
    path('subject/', SubjectListView.as_view(), name='subject_list'),
    path('subject/<slug:slug>/', CourseListBySubjectView.as_view(), name='course_list_by_subject'),
    path('course/<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('verify/', verify, name='verify'),
    path('resend/', resend_code, name='resend'),
]
