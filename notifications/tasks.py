from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_application_received_email(
    employer_email, employer_name, job_title, applicant_name
):
    try:
        subject = f"New Application Received for {job_title}"
        message = f"""
    Hi {employer_name},

    You have received a new application for: {job_title}
    Applicant: {applicant_name}

    Login to your dashboard to review.

    Best regards,
    CareerStack Team
        """
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[employer_email],
            fail_silently=False,
        )
        print(f"✅ Email sent to {employer_email}")
        return f"Email sent to {employer_email}"
    except Exception as e:
        print(f"❌ Email failed: {str(e)}")
        raise e


@shared_task
def send_application_status_email(
    applicant_email, applicant_name, job_title, status, employer_note=None
):
    try:
        status_messages = {
            'reviewed': f"Your application for {job_title} has been reviewed.",
            'shortlisted': f"Congratulations! You have been shortlisted for {job_title}.",
            'rejected': f"Your application for {job_title} was not selected.",
            'accepted': f"Congratulations! Your application for {job_title} has been accepted!",
        }
        subject = f"Application Update — {job_title}"
        message = f"""
    Hi {applicant_name},

    {status_messages.get(status, f'Your application status updated to {status}.')}
        """
        if employer_note:
            message += f"\n\nMessage from employer:\n{employer_note}"

        message += "\n\nLogin to CareerStack to track your applications.\n\nBest regards,\nCareerStack Team"

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[applicant_email],
            fail_silently=False,
        )
        print(f"✅ Status email sent to {applicant_email}")
        return f"Status email sent to {applicant_email}"
    except Exception as e:
        print(f"❌ Status email failed: {str(e)}")
        raise e
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