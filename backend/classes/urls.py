from django.urls import path
from .views import (
    AcademicYearListView,
    AcademicYearCreateView,
    ClassListView,
    ClassDetailView,
    ClassCreateView,
    ClassUpdateView,
    ClassDeleteView,
    SubjectListView,
    SubjectCreateView,
    SubjectUpdateView,
    SubjectDeleteView,
    ClassSubjectListView,
    ClassSubjectCreateView,
)

app_name = 'classes'

urlpatterns = [
    # Academic Years
    path('academic-years/', AcademicYearListView.as_view(), name='academic_year_list'),
    path('academic-years/create/', AcademicYearCreateView.as_view(), name='academic_year_create'),
    
    # Classes
    path('', ClassListView.as_view(), name='class_list'),
    path('<int:pk>/', ClassDetailView.as_view(), name='class_detail'),
    path('create/', ClassCreateView.as_view(), name='class_create'),
    path('<int:pk>/update/', ClassUpdateView.as_view(), name='class_update'),
    path('<int:pk>/delete/', ClassDeleteView.as_view(), name='class_delete'),
    
    # Subjects
    path('subjects/', SubjectListView.as_view(), name='subject_list'),
    path('subjects/create/', SubjectCreateView.as_view(), name='subject_create'),
    path('subjects/<int:pk>/update/', SubjectUpdateView.as_view(), name='subject_update'),
    path('subjects/<int:pk>/delete/', SubjectDeleteView.as_view(), name='subject_delete'),
    
    # Class Subjects
    path('class-subjects/', ClassSubjectListView.as_view(), name='class_subject_list'),
    path('class-subjects/create/', ClassSubjectCreateView.as_view(), name='class_subject_create'),
]