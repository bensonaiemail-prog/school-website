from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Avg
from django.http import HttpResponse
from .models import Term, Result, Attendance, Fee
from .pdf_generator import generate_report_card
from .serializers import (
    TermSerializer,
    ResultListSerializer,
    ResultDetailSerializer,
    ResultCreateSerializer,
    StudentResultsSummarySerializer,
    AttendanceSerializer,
    AttendanceCreateSerializer,
    FeeSerializer,
    FeeCreateSerializer
)
from students.models import Student

class IsTeacherOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and 
                (request.user.is_admin or request.user.is_teacher))


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


# Term Views
class TermListView(generics.ListAPIView):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
    permission_classes = [permissions.IsAuthenticated]


class TermCreateView(generics.CreateAPIView):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
    permission_classes = [IsAdminUser]


# Result Views
class ResultListView(generics.ListAPIView):
    serializer_class = ResultListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Result.objects.all()
        
        # Filter by student if provided
        student_id = self.request.query_params.get('student', None)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        # Filter by term if provided
        term_id = self.request.query_params.get('term', None)
        if term_id:
            queryset = queryset.filter(term_id=term_id)
        
        # Parents can only see their children's results
        if self.request.user.is_parent:
            children_ids = self.request.user.children.values_list('id', flat=True)
            queryset = queryset.filter(student_id__in=children_ids)
        
        return queryset


class ResultDetailView(generics.RetrieveAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResultCreateView(generics.CreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultCreateSerializer
    permission_classes = [IsTeacherOrAdmin]


class ResultUpdateView(generics.UpdateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultCreateSerializer
    permission_classes = [IsTeacherOrAdmin]


class ResultDeleteView(generics.DestroyAPIView):
    queryset = Result.objects.all()
    permission_classes = [IsAdminUser]


class StudentResultsSummaryView(APIView):
    """
    Get comprehensive results summary for a student in a specific term
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, student_id, term_id):
        # Check permissions and get student
        try:
            if request.user.is_parent:
                # Parents can only view their children
                student = Student.objects.get(id=student_id, parent=request.user, is_active=True)
            else:
                # Admin/Teachers can view any student
                student = Student.objects.get(id=student_id)
            
            term = Term.objects.get(id=term_id)
        except Student.DoesNotExist:
            if request.user.is_parent:
                return Response(
                    {'error': 'You can only view your children\'s results'},
                    status=status.HTTP_403_FORBIDDEN
                )
            return Response(
                {'error': 'Student not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Term.DoesNotExist:
            return Response(
                {'error': 'Term not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get all results for this student and term
        results = Result.objects.filter(student=student, term=term)
        
        # Calculate totals (handle empty results case)
        total_marks_obtained = results.aggregate(Sum('marks_obtained'))['marks_obtained__sum'] or 0
        total_marks_possible = results.aggregate(Sum('total_marks'))['total_marks__sum'] or 0
        overall_percentage = (total_marks_obtained / total_marks_possible * 100) if total_marks_possible > 0 else 0
        
        # Calculate overall grade
        if total_marks_possible == 0:
            overall_grade = None
        elif overall_percentage >= 90:
            overall_grade = 'A+'
        elif overall_percentage >= 80:
            overall_grade = 'A'
        elif overall_percentage >= 70:
            overall_grade = 'B+'
        elif overall_percentage >= 60:
            overall_grade = 'B'
        elif overall_percentage >= 50:
            overall_grade = 'C'
        elif overall_percentage >= 40:
            overall_grade = 'D'
        else:
            overall_grade = 'F'
        
        data = {
            'student_id': student.id,
            'student_name': student.full_name,
            'term_id': term.id,
            'term_display': str(term),
            'results': ResultListSerializer(results, many=True).data,
            'total_marks_obtained': float(total_marks_obtained),
            'total_marks_possible': float(total_marks_possible),
            'overall_percentage': round(overall_percentage, 2),
            'overall_grade': overall_grade,
            'has_results': results.exists(),
        }
        
        return Response(data)


class StudentPerformanceTrendView(APIView):
    """
    Get student performance across all terms (for trend analysis)
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, student_id):
        # Check permissions and get student
        try:
            if request.user.is_parent:
                # Parents can only view their children
                student = Student.objects.get(id=student_id, parent=request.user, is_active=True)
            else:
                # Admin/Teachers can view any student
                student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            if request.user.is_parent:
                return Response(
                    {'error': 'You can only view your children\'s results'},
                    status=status.HTTP_403_FORBIDDEN
                )
            return Response(
                {'error': 'Student not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get all terms that have results for this student
        terms_with_results = Term.objects.filter(
            results__student=student
        ).distinct().order_by('start_date', 'term_number')
        
        performance_data = []
        
        for term in terms_with_results:
            results = Result.objects.filter(student=student, term=term)
            
            if results.exists():
                total_marks_obtained = results.aggregate(Sum('marks_obtained'))['marks_obtained__sum'] or 0
                total_marks_possible = results.aggregate(Sum('total_marks'))['total_marks__sum'] or 0
                overall_percentage = (total_marks_obtained / total_marks_possible * 100) if total_marks_possible > 0 else 0
                
                # Calculate overall grade
                if overall_percentage >= 90:
                    overall_grade = 'A+'
                elif overall_percentage >= 80:
                    overall_grade = 'A'
                elif overall_percentage >= 70:
                    overall_grade = 'B+'
                elif overall_percentage >= 60:
                    overall_grade = 'B'
                elif overall_percentage >= 50:
                    overall_grade = 'C'
                elif overall_percentage >= 40:
                    overall_grade = 'D'
                else:
                    overall_grade = 'F'
                
                performance_data.append({
                    'term_id': term.id,
                    'term_display': str(term),
                    'term_number': term.term_number,
                    'academic_year': term.academic_year.year,
                    'overall_percentage': round(overall_percentage, 2),
                    'overall_grade': overall_grade,
                    'total_marks_obtained': float(total_marks_obtained),
                    'total_marks_possible': float(total_marks_possible),
                })
        
        return Response({
            'student_id': student.id,
            'student_name': student.full_name,
            'performance_trend': performance_data
        })


# Attendance Views
class AttendanceListView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Attendance.objects.all()
        
        # Filter by student
        student_id = self.request.query_params.get('student', None)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        # Filter by date
        date = self.request.query_params.get('date', None)
        if date:
            queryset = queryset.filter(date=date)
        
        # Parents can only see their children's attendance
        if self.request.user.is_parent:
            children_ids = self.request.user.children.values_list('id', flat=True)
            queryset = queryset.filter(student_id__in=children_ids)
        
        return queryset


class AttendanceCreateView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceCreateSerializer
    permission_classes = [IsTeacherOrAdmin]


class AttendanceUpdateView(generics.UpdateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceCreateSerializer
    permission_classes = [IsTeacherOrAdmin]


# Fee Views
class FeeListView(generics.ListAPIView):
    serializer_class = FeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Fee.objects.all()
        
        # Filter by student
        student_id = self.request.query_params.get('student', None)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        # Parents can only see their children's fees
        if self.request.user.is_parent:
            children_ids = self.request.user.children.values_list('id', flat=True)
            queryset = queryset.filter(student_id__in=children_ids)
        
        return queryset


class FeeCreateView(generics.CreateAPIView):
    queryset = Fee.objects.all()
    serializer_class = FeeCreateSerializer
    permission_classes = [IsAdminUser]


class FeeUpdateView(generics.UpdateAPIView):
    queryset = Fee.objects.all()
    serializer_class = FeeCreateSerializer
    permission_classes = [IsAdminUser]


class DownloadReportCardView(APIView):
    """
    Download PDF report card for a student
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, student_id, term_id):
        # Check permissions
        if request.user.is_parent:
            if not request.user.children.filter(id=student_id).exists():
                return Response(
                    {'error': 'You can only download your children\'s reports'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        try:
            student = Student.objects.get(id=student_id)
            term = Term.objects.get(id=term_id)
        except (Student.DoesNotExist, Term.DoesNotExist):
            return Response(
                {'error': 'Student or Term not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Generate PDF
        pdf_buffer = generate_report_card(student, term)
        
        # Create response
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        filename = f"Report_Card_{student.student_id}_{term.academic_year.year}_Term{term.term_number}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response