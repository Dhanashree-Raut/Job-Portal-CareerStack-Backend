from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_application_received_email(
    employer_email,
    employer_name,
    job_title,
    applicant_name
):
    """
    Sends email to employer when someone applies to their job.
    
    @shared_task means this function becomes a Celery task.
    It can be called normally OR run in background via Celery.
    """
    subject = f"New Application Received for {job_title}"
    message = f"""
    Hi {employer_name},

    You have received a new application for your job posting: {job_title}

    Applicant Name: {applicant_name}

    Please login to your dashboard to review the application.

    Best regards,
    Job Board Team
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[employer_email],
        fail_silently=False,
    )

    return f"Application email sent to {employer_email}"


@shared_task
def send_application_status_email(
    applicant_email,
    applicant_name,
    job_title,
    status,
    employer_note=None
):
    """
    Sends email to job seeker when their application status changes.
    Status can be: reviewed, shortlisted, rejected, accepted
    """

    # Customize message based on status
    status_messages = {
        'reviewed': f"Your application for {job_title} has been reviewed by the employer.",
        'shortlisted': f"Congratulations! You have been shortlisted for {job_title}.",
        'rejected': f"We regret to inform you that your application for {job_title} was not selected.",
        'accepted': f"Congratulations! Your application for {job_title} has been accepted!",
    }

    subject = f"Application Update — {job_title}"
    message = f"""
    Hi {applicant_name},

    {status_messages.get(status, f'Your application status has been updated to {status}.')}
    """

    # Add employer note if provided
    if employer_note:
        message += f"""
    
    Message from employer:
    {employer_note}
    """

    message += """

    Login to your dashboard to track all your applications.

    Best regards,
    Job Board Team
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[applicant_email],
        fail_silently=False,
    )

    return f"Status email sent to {applicant_email}"