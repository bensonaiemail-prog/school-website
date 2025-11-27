from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Student
from .serializers import (
    StudentListSerializer,
    StudentDetailSerializer,
    StudentCreateSerializer
)

class IsAdminOrTeacher(permissions.BasePermission):
    """
    Allow admins and teachers
    """
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and 
                (request.user.is_admin or request.user.is_teacher))


class IsParentOfStudent(permissions.BasePermission):
    """
    Allow parents to access their own children
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin or request.user.is_teacher:
            return True
        return obj.parent == request.user


class StudentListView(generics.ListAPIView):
    """
    List students
    - Admin/Teachers: See all students
    - Parents: See only their children
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin or user.is_teacher:
            return Student.objects.filter(is_active=True)
        elif user.is_parent:
            return Student.objects.filter(parent=user, is_active=True)
        
        return Student.objects.none()
    
    def get_serializer_class(self):
        return StudentListSerializer


class StudentDetailView(generics.RetrieveAPIView):
    """
    Get student details
    - Admin/Teachers: Can view any student
    - Parents: Can only view their children
    """
    queryset = Student.objects.filter(is_active=True)
    serializer_class = StudentDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsParentOfStudent]


class StudentCreateView(generics.CreateAPIView):
    """
    Create student
    - Admin: Can create for any parent
    - Parents: Can create for themselves
    """
    queryset = Student.objects.all()
    serializer_class = StudentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        if request.user.role == 'TEACHER':
            return Response(
                {'error': 'Teachers cannot create student records'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().create(request, *args, **kwargs)


class StudentUpdateView(generics.UpdateAPIView):
    """
    Update student
    - Admin: Can update any student
    - Parents: Can update their own children
    """
    queryset = Student.objects.all()
    serializer_class = StudentDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsParentOfStudent]


class StudentDeleteView(generics.DestroyAPIView):
    """
    Delete (deactivate) student - Admin only
    """
    queryset = Student.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return Response(
                {'error': 'Only admins can delete students'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().delete(request, *args, **kwargs)
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.is_active = False
        instance.save()


class MyChildrenView(generics.ListAPIView):
    """
    Get current parent's children
    """
    serializer_class = StudentDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'PARENT':
            return Student.objects.filter(
                parent=self.request.user, 
                is_active=True
            )
        return Student.objects.none()