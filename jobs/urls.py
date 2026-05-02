from django.urls import path
from . import views

urlpatterns = [
    # Job endpoints
    path('', views.JobListCreateView.as_view(), name='job-list-create'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    path('my-jobs/', views.EmployerJobListView.as_view(), name='my-jobs'),

    # Application endpoints
    path('<int:job_id>/apply/', views.ApplyJobView.as_view(), name='apply-job'),
    path('<int:job_id>/applications/', views.JobApplicationListView.as_view(), name='job-applications'),
    path('my-applications/', views.MyApplicationsView.as_view(), name='my-applications'),
    path('applications/<int:pk>/status/', views.UpdateApplicationStatusView.as_view(), name='update-application-status'),
]