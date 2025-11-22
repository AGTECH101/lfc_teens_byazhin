# lfc_teens_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ADD health check endpoint
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "healthy", "message": "Server is running"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),  # CHANGED from 'app' to 'lfc_teens'
    path('health/', health_check, name='health_check'),  # ADDED for Render health checks
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)