from django.urls import path
from .views import (
    TermListView,
    TermCreateView,
    ResultListView,
    ResultDetailView,
    ResultCreateView,
    ResultUpdateView,
    ResultDeleteView,
    StudentResultsSummaryView,
    AttendanceListView,
    AttendanceCreateView,
    AttendanceUpdateView,
    FeeListView,
    FeeCreateView,
    FeeUpdateView,
    DownloadReportCardView,
)

app_name = 'results'

urlpatterns = [
    # Terms
    path('terms/', TermListView.as_view(), name='term_list'),
    path('terms/create/', TermCreateView.as_view(), name='term_create'),
    
    # Results
    path('', ResultListView.as_view(), name='result_list'),
    path('<int:pk>/', ResultDetailView.as_view(), name='result_detail'),
    path('create/', ResultCreateView.as_view(), name='result_create'),
    path('<int:pk>/update/', ResultUpdateView.as_view(), name='result_update'),
    path('<int:pk>/delete/', ResultDeleteView.as_view(), name='result_delete'),
    path('summary/<int:student_id>/<int:term_id>/', StudentResultsSummaryView.as_view(), name='results_summary'),
    path('report-card/<int:student_id>/<int:term_id>/', DownloadReportCardView.as_view(), name='download_report_card'),
    
    # Attendance
    path('attendance/', AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/create/', AttendanceCreateView.as_view(), name='attendance_create'),
    path('attendance/<int:pk>/update/', AttendanceUpdateView.as_view(), name='attendance_update'),
    
    # Fees
    path('fees/', FeeListView.as_view(), name='fee_list'),
    path('fees/create/', FeeCreateView.as_view(), name='fee_create'),
    path('fees/<int:pk>/update/', FeeUpdateView.as_view(), name='fee_update'),
]