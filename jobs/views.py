from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Job, Application
from .serializers import (
    JobSerializer,
    ApplicationSerializer,
    ApplicationStatusSerializer
)
from .permissions import (
    IsEmployer,
    IsJobSeeker,
    IsEmployerOrReadOnly,
    IsOwnerOrReadOnly
)

from notifications.tasks import (
    send_application_received_email,
    send_application_confirmation_email,
    send_application_status_email,
    send_job_created_email,
)

# -----------------------------------------------
# JOB VIEWS
# -----------------------------------------------

class JobListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/jobs/          — List all active jobs (anyone can view)
    POST /api/jobs/          — Create a new job (employers only)
    """
    serializer_class = JobSerializer
    permission_classes = [IsEmployerOrReadOnly]

    def get_queryset(self):
        queryset = Job.objects.filter(status='active')

        job_type = self.request.query_params.get('job_type')
        location = self.request.query_params.get('location')
        experience_level = self.request.query_params.get('experience_level')
        search = self.request.query_params.get('search')

        if job_type:
            queryset = queryset.filter(job_type=job_type)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if experience_level:
            queryset = queryset.filter(experience_level=experience_level)
        if search:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(skills_required__icontains=search)
            )

        return queryset

    def perform_create(self, serializer):
        if not self.request.user.role == 'employer':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only employers can post jobs.")

        job = serializer.save(employer=self.request.user)

        # ✅ Email employer confirming job was posted
        send_job_created_email.delay(
            employer_email=self.request.user.email,
            employer_name=self.request.user.username,
            job_title=job.title,
            location=job.location,
            job_type=job.job_type,
        )


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/jobs/<id>/   — View job details (anyone)
    PUT    /api/jobs/<id>/   — Update job (owner employer only)
    DELETE /api/jobs/<id>/   — Delete job (owner employer only)
    """
    serializer_class = JobSerializer
    permission_classes = [IsEmployerOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Job.objects.all()


class EmployerJobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsEmployer]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Job.objects.none()
        return Job.objects.filter(employer=self.request.user)

# -----------------------------------------------
# APPLICATION VIEWS
# -----------------------------------------------

class ApplyJobView(generics.CreateAPIView):
    """
    POST /api/jobs/<id>/apply/   — Job seeker applies to a job
    """
    serializer_class = ApplicationSerializer
    permission_classes = [IsJobSeeker]

    def perform_create(self, serializer):
        job = get_object_or_404(Job, id=self.kwargs['job_id'])

        if job.status != 'active':
            from rest_framework.exceptions import ValidationError
            raise ValidationError("This job is no longer accepting applications.")

        if Application.objects.filter(
            applicant=self.request.user,
            job=job
        ).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError("You have already applied to this job.")

        serializer.save(
            applicant=self.request.user,
            job=job
        )

        # ✅ Email employer — new application received
        send_application_received_email.delay(
            employer_email=job.employer.email,
            employer_name=job.employer.username,
            job_title=job.title,
            applicant_name=self.request.user.username,
        )

        # ✅ Email job seeker — application confirmation
        send_application_confirmation_email.delay(
            applicant_email=self.request.user.email,
            applicant_name=self.request.user.username,
            job_title=job.title,
            company_name=job.employer.company_name or job.employer.username,
        )


class JobApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsEmployer]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Application.objects.none()
        job = get_object_or_404(
            Job,
            id=self.kwargs['job_id'],
            employer=self.request.user
        )
        return Application.objects.filter(job=job)


class MyApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsJobSeeker]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Application.objects.none()
        return Application.objects.filter(applicant=self.request.user)


class UpdateApplicationStatusView(generics.UpdateAPIView):
    serializer_class = ApplicationStatusSerializer
    permission_classes = [IsEmployer]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Application.objects.none()
        return Application.objects.filter(job__employer=self.request.user)

    def update(self, request, *args, **kwargs):
        application = self.get_object()
        serializer = self.get_serializer(
            application,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # ✅ Email job seeker — status updated
        send_application_status_email.delay(
            applicant_email=application.applicant.email,
            applicant_name=application.applicant.username,
            job_title=application.job.title,
            status=request.data.get('status'),
            employer_note=request.data.get('employer_note'),
        )

        return Response({
            "message": "Application status updated successfully.",
            "application": serializer.data
        }, status=status.HTTP_200_OK)