from django.contrib import admin
from .models import Term, Result, Attendance, Fee

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'start_date', 'end_date', 'is_current']
    list_filter = ['academic_year', 'is_current']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'term', 'marks_obtained', 'grade']
    list_filter = ['term', 'subject', 'grade']
    search_fields = ['student__first_name', 'student__last_name']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'class_obj']
    list_filter = ['status', 'date', 'class_obj']
    search_fields = ['student__first_name', 'student__last_name']

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'term', 'amount', 'amount_paid', 'balance', 'status']
    list_filter = ['status', 'term']
    search_fields = ['student__first_name', 'student__last_name']