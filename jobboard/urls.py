from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger schema configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Job Board API",
        default_version='v1',
        description="""
        Job Board API documentation.
        
        ## Authentication
        Use JWT tokens for authentication.
        1. Register or Login to get tokens
        2. Click Authorize button and enter: Bearer your_access_token
        
        ## Roles
        - **Job Seeker** — can apply to jobs, track applications
        - **Employer** — can post jobs, manage applications
        - **Admin** — manages all users and listings
        """,
        contact=openapi.Contact(email="admin@jobboard.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/accounts/', include('accounts.urls')),
    path('api/jobs/', include('jobs.urls')),

    # Swagger UI — beautiful interactive docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),

    # ReDoc — alternative clean documentation
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)