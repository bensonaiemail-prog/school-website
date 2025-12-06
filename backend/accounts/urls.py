from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserProfileView,
    ChangePasswordView,
    PendingTeachersView,
    ApproveTeacherView
)

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    
    # Teacher approval (Admin only)
    path('teachers/pending/', PendingTeachersView.as_view(), name='pending_teachers'),
    path('teachers/<int:user_id>/approve/', ApproveTeacherView.as_view(), name='approve_teacher'),

    # Parent
    # Additional endpoints for parent functionalities can be added here
    path('parent/dashboard/', UserProfileView.as_view(), name='parent_dashboard'),
    path('parent/children/', UserProfileView.as_view(), name='parent_children'),
    path('parent/notifications/', UserProfileView.as_view(), name='parent_notifications'),
    
]