from rest_framework import serializers
from .models import Job, Application
from accounts.serializers import UserProfileSerializer


class JobSerializer(serializers.ModelSerializer):
    """
    Serializer for Job model.
    Used for creating, updating and listing jobs.
    """

    # Show employer details as nested object instead of just ID
    employer_details = UserProfileSerializer(
        source='employer',
        read_only=True
    )

    # Extra fields calculated from model
    total_applications = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'employer', 'employer_details',
            'title', 'description', 'requirements',
            'location', 'salary_min', 'salary_max',
            'job_type', 'experience_level', 'skills_required',
            'status', 'deadline', 'total_applications',
            'created_at', 'updated_at'
        ]
        # employer is set automatically from logged in user
        # so we make it read only
        read_only_fields = ['employer', 'created_at', 'updated_at']

    def get_total_applications(self, obj):
        """
        SerializerMethodField calls this method automatically.
        Returns count of applications for this job.
        Method name must be get_<field_name>
        """
        return obj.applications.count()


class ApplicationSerializer(serializers.ModelSerializer):
    applicant_details = UserProfileSerializer(
        source='applicant',
        read_only=True
    )
    job_details = JobSerializer(
        source='job',
        read_only=True
    )

    class Meta:
        model = Application
        fields = [
            'id', 'applicant', 'applicant_details',
            'job', 'job_details',
            'cover_letter', 'resume', 'status',
            'employer_note', 'applied_at', 'updated_at'
        ]
        read_only_fields = [
            'applicant', 'job',  # ✅ Add job here
            'status', 'employer_note',
            'applied_at', 'updated_at'
        ]

class ApplicationStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for employer to update application status.
    Only exposes status and employer_note fields.
    """

    class Meta:
        model = Application
        fields = ['id', 'status', 'employer_note']
        extra_kwargs = {
            'employer_note': {'required': False, 'allow_blank': True},
            'status': {'required': True},
        }