import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

# APIClient is like Postman but in code
# It lets us make HTTP requests in tests


@pytest.fixture
def client():
    """
    Fixture — a reusable setup that runs before each test.
    Creates a fresh APIClient for every test.
    """
    return APIClient()


@pytest.fixture
def job_seeker(db):
    """
    Creates a job seeker user for testing.
    db fixture gives access to the test database.
    """
    user = User.objects.create_user(
        email='jobseeker@test.com',
        username='jobseeker',
        password='Test@1234',
        role='job_seeker'
    )
    return user


@pytest.fixture
def employer(db):
    """
    Creates an employer user for testing.
    """
    user = User.objects.create_user(
        email='employer@test.com',
        username='employer',
        password='Test@1234',
        role='employer',
        company_name='Test Company'
    )
    return user


@pytest.fixture
def job_seeker_client(client, job_seeker):
    """
    Returns an authenticated client for job seeker.
    So we don't need to login in every test.
    """
    response = client.post('/api/accounts/login/', {
        'email': 'jobseeker@test.com',
        'password': 'Test@1234'
    }, format='json')
    token = response.data['tokens']['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


@pytest.fixture
def employer_client(client, employer):
    """
    Returns an authenticated client for employer.
    """
    response = client.post('/api/accounts/login/', {
        'email': 'employer@test.com',
        'password': 'Test@1234'
    }, format='json')
    token = response.data['tokens']['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


# -----------------------------------------------
# REGISTRATION TESTS
# -----------------------------------------------

@pytest.mark.django_db
def test_register_job_seeker(client):
    """
    Test that a job seeker can register successfully.
    @pytest.mark.django_db allows this test to use the database.
    """
    response = client.post('/api/accounts/register/', {
        'email': 'newuser@test.com',
        'username': 'newuser',
        'password': 'Test@1234',
        'password2': 'Test@1234',
        'role': 'job_seeker'
    }, format='json')

    # Assert means "this must be true or test fails"
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['user']['email'] == 'newuser@test.com'
    assert response.data['user']['role'] == 'job_seeker'
    assert 'tokens' in response.data


@pytest.mark.django_db
def test_register_employer(client):
    """
    Test that an employer can register successfully.
    """
    response = client.post('/api/accounts/register/', {
        'email': 'employer@test.com',
        'username': 'employer',
        'password': 'Test@1234',
        'password2': 'Test@1234',
        'role': 'employer',
        'company_name': 'Test Company'
    }, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['user']['role'] == 'employer'


@pytest.mark.django_db
def test_register_password_mismatch(client):
    """
    Test that registration fails when passwords don't match.
    We test FAILURE cases too — not just success!
    """
    response = client.post('/api/accounts/register/', {
        'email': 'test@test.com',
        'username': 'test',
        'password': 'Test@1234',
        'password2': 'WrongPassword',
        'role': 'job_seeker'
    }, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_register_duplicate_email(client, job_seeker):
    """
    Test that registration fails with duplicate email.
    job_seeker fixture already created a user with jobseeker@test.com
    """
    response = client.post('/api/accounts/register/', {
        'email': 'jobseeker@test.com',  # Already exists
        'username': 'another',
        'password': 'Test@1234',
        'password2': 'Test@1234',
        'role': 'job_seeker'
    }, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


# -----------------------------------------------
# LOGIN TESTS
# -----------------------------------------------

@pytest.mark.django_db
def test_login_success(client, job_seeker):
    """
    Test successful login returns tokens.
    """
    response = client.post('/api/accounts/login/', {
        'email': 'jobseeker@test.com',
        'password': 'Test@1234'
    }, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'tokens' in response.data
    assert 'access' in response.data['tokens']
    assert 'refresh' in response.data['tokens']


@pytest.mark.django_db
def test_login_wrong_password(client, job_seeker):
    """
    Test login fails with wrong password.
    """
    response = client.post('/api/accounts/login/', {
        'email': 'jobseeker@test.com',
        'password': 'WrongPassword'
    }, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_login_nonexistent_user(client):
    """
    Test login fails for user that doesn't exist.
    """
    response = client.post('/api/accounts/login/', {
        'email': 'nobody@test.com',
        'password': 'Test@1234'
    }, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# -----------------------------------------------
# PROFILE TESTS
# -----------------------------------------------

@pytest.mark.django_db
def test_get_profile(job_seeker_client):
    """
    Test authenticated user can view their profile.
    """
    response = job_seeker_client.get('/api/accounts/profile/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == 'jobseeker@test.com'


@pytest.mark.django_db
def test_profile_requires_auth(client):
    """
    Test that unauthenticated request cannot access profile.
    """
    response = client.get('/api/accounts/profile/')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_profile(job_seeker_client):
    """
    Test user can update their profile.
    """
    response = job_seeker_client.put('/api/accounts/profile/', {
        'username': 'updateduser',
        'phone': '9876543210',
        'skills': 'Python, Django'
    }, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['phone'] == '9876543210'
    assert response.data['skills'] == 'Python, Django'