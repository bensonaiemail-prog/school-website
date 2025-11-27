from rest_framework import serializers
from .models import Term, Result, Attendance, Fee

class TermSerializer(serializers.ModelSerializer):
    academic_year_display = serializers.CharField(source='academic_year.year', read_only=True)
    
    class Meta:
        model = Term
        fields = '__all__'


class ResultListSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    term_display = serializers.CharField(source='term.__str__', read_only=True)
    percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Result
        fields = ['id', 'student', 'student_name', 'subject', 'subject_name', 
                  'term', 'term_display', 'marks_obtained', 'total_marks', 
                  'percentage', 'grade', 'remarks']


class ResultDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    term_display = serializers.CharField(source='term.__str__', read_only=True)
    entered_by_name = serializers.CharField(source='entered_by.full_name', read_only=True)
    percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Result
        fields = '__all__'


class ResultCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        exclude = ['entered_by', 'grade', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Set the entered_by to current user's teacher profile
        request = self.context['request']
        if hasattr(request.user, 'teacher_profile'):
            validated_data['entered_by'] = request.user.teacher_profile
        return super().create(validated_data)


class StudentResultsSummarySerializer(serializers.Serializer):
    """
    Summary of student results for a specific term
    """
    student_id = serializers.IntegerField()
    student_name = serializers.CharField()
    term_id = serializers.IntegerField()
    term_display = serializers.CharField()
    results = ResultListSerializer(many=True)
    total_marks_obtained = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_marks_possible = serializers.DecimalField(max_digits=10, decimal_places=2)
    overall_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    overall_grade = serializers.CharField()


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    class_name = serializers.CharField(source='class_obj.name', read_only=True)
    marked_by_name = serializers.CharField(source='marked_by.full_name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'


class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        exclude = ['marked_by', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        request = self.context['request']
        if hasattr(request.user, 'teacher_profile'):
            validated_data['marked_by'] = request.user.teacher_profile
        return super().create(validated_data)


class FeeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    term_display = serializers.CharField(source='term.__str__', read_only=True)
    balance = serializers.ReadOnlyField()
    
    class Meta:
        model = Fee
        fields = '__all__'


class FeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        exclude = ['created_at', 'updated_at', 'status']