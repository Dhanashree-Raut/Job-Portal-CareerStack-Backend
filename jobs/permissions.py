from rest_framework.permissions import BasePermission


class IsEmployer(BasePermission):
    """
    Only allows access to users with 'employer' role.
    Used for: creating jobs, managing applications
    """
    message = "Only employers can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'employer'
        )


class IsJobSeeker(BasePermission):
    """
    Only allows access to users with 'job_seeker' role.
    Used for: applying to jobs, tracking applications
    """
    message = "Only job seekers can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'job_seeker'
        )


class IsEmployerOrReadOnly(BasePermission):
    """
    Employers can do everything.
    Others can only READ (GET requests).
    Used for: job listings — anyone can view but only employer can post
    """
    message = "Only employers can modify jobs."

    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD, OPTIONS — read only requests
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return (
            request.user.is_authenticated and
            request.user.role == 'employer'
        )


class IsOwnerOrReadOnly(BasePermission):
    """
    Object level permission.
    Only the owner of an object can edit or delete it.
    Used for: employer can only edit/delete THEIR OWN jobs
    """
    message = "You can only modify your own content."

    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for any request
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Write permissions only for the owner
        # obj.employer checks the job's employer field
        return obj.employer == request.user