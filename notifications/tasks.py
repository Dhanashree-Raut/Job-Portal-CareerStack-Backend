from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import threading


def send_email_async(subject, message, recipient):
    """Send email in background thread so it doesn't block the API"""
    def _send():
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient],
                fail_silently=True,
            )
            print(f"✅ Email sent to {recipient}")
        except Exception as e:
            print(f"❌ Email failed: {str(e)}")
    
    thread = threading.Thread(target=_send)
    thread.daemon = True
    thread.start()


@shared_task
def send_application_received_email(
    employer_email, employer_name, job_title, applicant_name
):
    subject = f"New Application Received for {job_title}"
    message = f"""
Hi {employer_name},

You have received a new application for: {job_title}
Applicant: {applicant_name}

Login to your dashboard to review.

Best regards,
CareerStack Team
    """
    send_email_async(subject, message, employer_email)
    return f"Email queued for {employer_email}"


@shared_task
def send_application_status_email(
    applicant_email, applicant_name, job_title, status, employer_note=None
):
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

    send_email_async(subject, message, applicant_email)
    return f"Email queued for {applicant_email}"