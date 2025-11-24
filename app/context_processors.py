# app/context_processors.py
from django.conf import settings

def seo_context(request):
    return {
        'site_name': getattr(settings, 'SITE_NAME', 'LFC Teens Byazhin'),
        'site_description': getattr(settings, 'SITE_DESCRIPTION', 'Christian teens ministry in Byazhin, Abuja'),
        'site_keywords': getattr(settings, 'SITE_KEYWORDS', 'LFC Teens, Christian youth, Abuja church'),
    }