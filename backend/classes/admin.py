from django.contrib import admin
from .models import AcademicYear, Class, Subject, ClassSubject

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['year', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade_level', 'section', 'academic_year', 'class_teacher', 'student_count']
    list_filter = ['grade_level', 'academic_year']
    search_fields = ['name', 'section']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'grade_level']
    list_filter = ['grade_level']
    search_fields = ['name', 'code']

@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ['class_obj', 'subject', 'teacher']
    list_filter = ['class_obj', 'subject']