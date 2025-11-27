from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Teacher
from .serializers import (
    TeacherPublicSerializer,
    TeacherDetailSerializer,
    TeacherCreateSerializer
)

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admins
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class TeacherListView(generics.ListAPIView):
    """
    List all teachers
    GET: Public info for everyone, full details for admins
    """
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Teacher.objects.filter(is_active=True)
    
    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_admin:
            return TeacherDetailSerializer
        return TeacherPublicSerializer


class TeacherDetailView(generics.RetrieveAPIView):
    """
    Get single teacher details
    GET: Public info for everyone, full details for admins
    """
    permission_classes = [permissions.AllowAny]
    queryset = Teacher.objects.filter(is_active=True)
    
    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_admin:
            return TeacherDetailSerializer
        return TeacherPublicSerializer


class TeacherCreateView(generics.CreateAPIView):
    """
    Create teacher profile (Teachers only, after account approval)
    POST: Create teacher profile
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Check if user is a teacher
        if request.user.role != 'TEACHER':
            return Response(
                {'error': 'Only teachers can create teacher profiles'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if teacher profile already exists
        if hasattr(request.user, 'teacher_profile'):
            return Response(
                {'error': 'Teacher profile already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().create(request, *args, **kwargs)


class TeacherUpdateView(generics.UpdateAPIView):
    """
    Update teacher profile
    PUT/PATCH: Update own profile or admin can update any
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        if self.request.user.is_admin:
            # Admin can update any teacher
            return super().get_object()
        else:
            # Teacher can only update their own profile
            return self.request.user.teacher_profile


class TeacherDeleteView(generics.DestroyAPIView):
    """
    Delete (deactivate) teacher
    DELETE: Admin only
    """
    queryset = Teacher.objects.all()
    permission_classes = [IsAdminUser]
    
    def perform_destroy(self, instance):
        # Soft delete - just deactivate
        instance.is_active = False
        instance.save()