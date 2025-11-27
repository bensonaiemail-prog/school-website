from rest_framework import generics, permissions
from .models import AcademicYear, Class, Subject, ClassSubject
from .serializers import (
    AcademicYearSerializer,
    ClassListSerializer,
    ClassDetailSerializer,
    SubjectSerializer,
    ClassSubjectSerializer
)

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


# Academic Year Views
class AcademicYearListView(generics.ListAPIView):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [permissions.IsAuthenticated]


class AcademicYearCreateView(generics.CreateAPIView):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [IsAdminUser]


# Class Views
class ClassListView(generics.ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Class.objects.all()
        # Filter by academic year if provided
        year = self.request.query_params.get('year', None)
        if year:
            queryset = queryset.filter(academic_year__year=year)
        return queryset


class ClassDetailView(generics.RetrieveAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClassCreateView(generics.CreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassDetailSerializer
    permission_classes = [IsAdminUser]


class ClassUpdateView(generics.UpdateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassDetailSerializer
    permission_classes = [IsAdminUser]


class ClassDeleteView(generics.DestroyAPIView):
    queryset = Class.objects.all()
    permission_classes = [IsAdminUser]


# Subject Views
class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubjectCreateView(generics.CreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminUser]


class SubjectUpdateView(generics.UpdateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminUser]


class SubjectDeleteView(generics.DestroyAPIView):
    queryset = Subject.objects.all()
    permission_classes = [IsAdminUser]


# ClassSubject Views
class ClassSubjectListView(generics.ListAPIView):
    queryset = ClassSubject.objects.all()
    serializer_class = ClassSubjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = ClassSubject.objects.all()
        class_id = self.request.query_params.get('class', None)
        if class_id:
            queryset = queryset.filter(class_obj_id=class_id)
        return queryset


class ClassSubjectCreateView(generics.CreateAPIView):
    queryset = ClassSubject.objects.all()
    serializer_class = ClassSubjectSerializer
    permission_classes = [IsAdminUser]