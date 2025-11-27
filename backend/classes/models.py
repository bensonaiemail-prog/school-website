from django.db import models
from teachers.models import Teacher

class AcademicYear(models.Model):
    """
    Academic year management
    """
    year = models.CharField(max_length=9, unique=True)  # e.g., "2024-2025"
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.year
    
    def save(self, *args, **kwargs):
        if self.is_current:
            # Set all other years to not current
            AcademicYear.objects.filter(is_current=True).update(is_current=False)
        super().save(*args, **kwargs)


class Class(models.Model):
    """
    Class/Grade model
    """
    name = models.CharField(max_length=50)  # e.g., "Grade 10A"
    grade_level = models.IntegerField()  # e.g., 10
    section = models.CharField(max_length=10)  # e.g., "A"
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name='classes'
    )
    class_teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_classes'
    )
    room_number = models.CharField(max_length=20, blank=True, null=True)
    capacity = models.IntegerField(default=30)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['grade_level', 'section']
        verbose_name_plural = 'Classes'
        unique_together = ['grade_level', 'section', 'academic_year']
    
    def __str__(self):
        return f"{self.name} ({self.academic_year.year})"
    
    @property
    def student_count(self):
        return self.students.filter(is_active=True).count()


class Subject(models.Model):
    """
    Subject model
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    grade_level = models.IntegerField()  # Which grade this subject is for
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['grade_level', 'name']
    
    def __str__(self):
        return f"{self.name} (Grade {self.grade_level})"


class ClassSubject(models.Model):
    """
    Link between Class, Subject, and Teacher
    A class can have multiple subjects, each taught by a teacher
    """
    class_obj = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='class_subjects'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='class_subjects'
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teaching_assignments'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['class_obj', 'subject']
    
    def __str__(self):
        return f"{self.class_obj.name} - {self.subject.name}"