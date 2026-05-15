from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


# ─────────────────────────────────────────────────────────
# 1. Welcome email on account creation
# ─────────────────────────────────────────────────────────
@shared_task
def send_welcome_email(email, username, role, phone=None, company_name=None, skills=None):
    try:
        is_employer = role == 'employer'

        subject = "Welcome to CareerStack! 🎉"

        if is_employer:
            role_label = 'Employer'
            extra_info = f"Company : {company_name or 'Not provided'}"
        else:
            role_label = 'Job Seeker'
            extra_info = f"Skills  : {skills or 'Not provided'}"

        message = f"""
Hi {username},

Welcome to CareerStack! Your account has been created successfully.

Here are your account details:

  Username : {username}
  Email    : {email}
  Role     : {role_label}
  Phone    : {phone or 'Not provided'}
  {extra_info}

{'You can now post jobs and manage applications from your dashboard.' if is_employer else 'You can now browse jobs and apply directly from your dashboard.'}

If you did not create this account, please contact us immediately.

Best regards,
CareerStack Team
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        print(f"✅ Welcome email sent to {email}")
    except Exception as e:
        print(f"❌ Welcome email failed: {str(e)}")


# ─────────────────────────────────────────────────────────
# 2. Employer receives email when someone applies to their job
# ─────────────────────────────────────────────────────────
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

Login to your dashboard to review the application and update the status.

Best regards,
CareerStack Team
        """
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[employer_email],
            fail_silently=False,
        )
        print(f"✅ Application received email sent to {employer_email}")
    except Exception as e:
        print(f"❌ Application received email failed: {str(e)}")


# ─────────────────────────────────────────────────────────
# 3. Job seeker receives confirmation email after applying
# ─────────────────────────────────────────────────────────
@shared_task
def send_application_confirmation_email(
    applicant_email, applicant_name, job_title, company_name
):
    try:
        subject = f"Application Submitted — {job_title} at {company_name}"
        message = f"""
Hi {applicant_name},

Your application has been successfully submitted!

Job Title : {job_title}
Company   : {company_name}

The employer will review your application and update you on the status.
You can track all your applications by logging into CareerStack.

Best of luck!

Best regards,
CareerStack Team
        """
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[applicant_email],
            fail_silently=False,
        )
        print(f"✅ Application confirmation email sent to {applicant_email}")
    except Exception as e:
        print(f"❌ Application confirmation email failed: {str(e)}")


# ─────────────────────────────────────────────────────────
# 4. Employer receives confirmation email when they post a job
# ─────────────────────────────────────────────────────────
@shared_task
def send_job_created_email(
    employer_email, employer_name, job_title, location, job_type
):
    try:
        subject = f"Your Job Has Been Posted — {job_title}"
        message = f"""
Hi {employer_name},

Your job posting is now live on CareerStack!

Job Title : {job_title}
Location  : {location}
Job Type  : {job_type.replace('_', ' ').title()}

Job seekers can now find and apply to your posting.
Login to your dashboard to manage applications.

Best regards,
CareerStack Team
        """
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[employer_email],
            fail_silently=False,
        )
        print(f"✅ Job created email sent to {employer_email}")
    except Exception as e:
        print(f"❌ Job created email failed: {str(e)}")


# ─────────────────────────────────────────────────────────
# 5. Job seeker receives status update email
# ─────────────────────────────────────────────────────────
@shared_task
def send_application_status_email(
    applicant_email, applicant_name, job_title, status, employer_note=None
):
    try:
        status_messages = {
            'reviewed':    f"Your application for {job_title} has been reviewed.",
            'shortlisted': f"Congratulations! You have been shortlisted for {job_title}.",
            'rejected':    f"Your application for {job_title} was not selected.",
            'accepted':    f"Congratulations! Your application for {job_title} has been accepted!",
        }
        subject = f"Application Update — {job_title}"
        message = f"""
Hi {applicant_name},

{status_messages.get(status, f'Your application status has been updated to: {status}.')}
        """
        if employer_note:
            message += f"\n\nMessage from employer:\n{employer_note}"

        message += "\n\nLogin to CareerStack to track all your applications.\n\nBest regards,\nCareerStack Team"

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[applicant_email],
            fail_silently=False,
        )
        print(f"✅ Status email sent to {applicant_email}")
    except Exception as e:
        print(f"❌ Status email failed: {str(e)}")