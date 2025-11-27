from rest_framework import serializers
from .models import AcademicYear, Class, Subject, ClassSubject

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'


class ClassListSerializer(serializers.ModelSerializer):
    class_teacher_name = serializers.CharField(source='class_teacher.full_name', read_only=True)
    academic_year_display = serializers.CharField(source='academic_year.year', read_only=True)
    student_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Class
        fields = ['id', 'name', 'grade_level', 'section', 'academic_year', 
                  'academic_year_display', 'class_teacher', 'class_teacher_name', 
                  'room_number', 'capacity', 'student_count']


class ClassDetailSerializer(serializers.ModelSerializer):
    class_teacher_name = serializers.CharField(source='class_teacher.full_name', read_only=True)
    academic_year_display = serializers.CharField(source='academic_year.year', read_only=True)
    student_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Class
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class ClassSubjectSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_obj.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.full_name', read_only=True)
    
    class Meta:
        model = ClassSubject
        fields = '__all__'