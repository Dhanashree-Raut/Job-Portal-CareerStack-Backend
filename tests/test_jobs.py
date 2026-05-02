import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from jobs.models import Job, Application

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def employer(db):
    return User.objects.create_user(
        email='employer@test.com',
        username='employer',
        password='Test@1234',
        role='employer',
        company_name='Test Company'
    )


@pytest.fixture
def job_seeker(db):
    return User.objects.create_user(
        email='jobseeker@test.com',
        username='jobseeker',
        password='Test@1234',
        role='job_seeker'
    )


@pytest.fixture
def employer_client(client, employer):
    response = client.post('/api/accounts/login/', {
        'email': 'employer@test.com',
        'password': 'Test@1234'
    }, format='json')
    token = response.data['tokens']['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


@pytest.fixture
def job_seeker_client(client, job_seeker):
    response = client.post('/api/accounts/login/', {
        'email': 'jobseeker@test.com',
        'password': 'Test@1234'
    }, format='json')
    token = response.data['tokens']['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


@pytest.fixture
def sample_job(db, employer):
    """
    Creates a sample job for testing.
    Other tests that need a job use this fixture.
    """
    return Job.objects.create(
        employer=employer,
        title='Django Developer',
        description='We need a Django developer',
        requirements='2 years experience',
        location='Mumbai',
        job_type='full_time',
        experience_level='mid',
        skills_required='Python, Django',
        status='active'
    )


# -----------------------------------------------
# JOB TESTS
# -----------------------------------------------

@pytest.mark.django_db
def test_employer_can_create_job(employer_client):
    """
    Test employer can post a new job.
    """
    response = employer_client.post('/api/jobs/', {
        'title': 'Django Developer',
        'description': 'We need a Django developer',
        'requirements': '2 years experience',
        'location': 'Mumbai',
        'job_type': 'full_time',
        'experience_level': 'mid',
        'skills_required': 'Python, Django',
        'status': 'active'
    }, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == 'Django Developer'


@pytest.mark.django_db
def test_job_seeker_cannot_create_job(job_seeker_client):
    """
    Test job seeker cannot post a job.
    This tests our permission system works correctly.
    """
    response = job_seeker_client.post('/api/jobs/', {
        'title': 'Django Developer',
        'description': 'Test',
        'requirements': 'Test',
        'location': 'Mumbai',
        'job_type': 'full_time',
        'experience_level': 'mid',
        'skills_required': 'Python',
        'status': 'active'
    }, format='json')

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_anyone_can_list_jobs(client, sample_job):
    """
    Test that job listing is public — no auth needed.
    """
    response = client.get('/api/jobs/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0


@pytest.mark.django_db
def test_job_search_filter(client, sample_job):
    """
    Test search filter works correctly.
    """
    response = client.get('/api/jobs/?search=Django')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0


@pytest.mark.django_db
def test_job_type_filter(client, sample_job):
    """
    Test job_type filter works.
    """
    response = client.get('/api/jobs/?job_type=full_time')

    assert response.status_code == status.HTTP_200_OK


# -----------------------------------------------
# APPLICATION TESTS
# -----------------------------------------------

@pytest.mark.django_db
def test_job_seeker_can_apply(client, job_seeker, employer):
    fresh_job = Job.objects.create(
        employer=employer,
        title='Fresh Test Job',
        description='Test description',
        requirements='Test requirements',
        location='Mumbai',
        job_type='full_time',
        experience_level='mid',
        skills_required='Python',
        status='active'
    )

    response = client.post('/api/accounts/login/', {
        'email': 'jobseeker@test.com',
        'password': 'Test@1234'
    }, format='json')
    token = response.data['tokens']['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.post(
        f'/api/jobs/{fresh_job.id}/apply/',
        {'cover_letter': 'I am interested in this position.'},
        format='json'
    )

    # Print actual error so we can see what's happening
    print("RESPONSE DATA:", response.data)
    print("STATUS CODE:", response.status_code)

    assert response.status_code == status.HTTP_201_CREATED
@pytest.mark.django_db
def test_cannot_apply_twice(job_seeker_client, job_seeker, sample_job):
    """
    Test job seeker cannot apply to same job twice.
    """
    # First application
    Application.objects.create(
        applicant=job_seeker,
        job=sample_job,
        cover_letter='First application'
    )

    # Try to apply again
    response = job_seeker_client.post(
        f'/api/jobs/{sample_job.id}/apply/',
        {'cover_letter': 'Second application'},
        format='json'
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_employer_cannot_apply(employer_client, sample_job):
    """
    Test employer cannot apply to a job.
    """
    response = employer_client.post(
        f'/api/jobs/{sample_job.id}/apply/',
        {'cover_letter': 'I want to apply'},
        format='json'
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_employer_can_update_application_status(
    employer_client,
    job_seeker,
    sample_job
):
    """
    Test employer can update application status.
    """
    # Create application directly in DB
    application = Application.objects.create(
        applicant=job_seeker,
        job=sample_job,
        cover_letter='Test application'
    )

    response = employer_client.put(
        f'/api/jobs/applications/{application.id}/status/',
        {
            'status': 'shortlisted',
            'employer_note': 'Great profile!'
        },
        format='json'
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['application']['status'] == 'shortlisted'


@pytest.mark.django_db
def test_job_seeker_can_view_own_applications(
    job_seeker_client,
    job_seeker,
    sample_job
):
    """
    Test job seeker can see their own applications.
    """
    Application.objects.create(
        applicant=job_seeker,
        job=sample_job,
        cover_letter='Test'
    )

    response = job_seeker_client.get('/api/jobs/my-applications/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1