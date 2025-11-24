# lfc_teens/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
import hashlib
import uuid
from .models import *

def home(request):
    try:
        contact_info = ContactInfo.objects.first()
    except ObjectDoesNotExist:
        contact_info = None

    context = {
        'hero': HeroSlide.objects.filter(is_active=True),
        'leaders': Leader.objects.filter(is_active=True),
        'bible_post': BiblePost.objects.filter(is_active=True),
        'announcement': Announcement.objects.filter(is_active=True),
        'testimony': Testimony.objects.filter(is_approved=True),
        'unit': MinistryUnit.objects.filter(is_active=True),
        'belief': Belief.objects.filter(is_active=True),
        'counselors': Leader.objects.filter(is_active=True, is_counselor=True),
        'contact_info': contact_info,
    }
    return render(request, 'index.html', context)

@require_POST
def add_like(request):
    post_id = request.POST.get('post_id')
    bible_post = get_object_or_404(BiblePost, id=post_id)
    
    # Create a unique viewer ID using browser fingerprinting
    # Combine IP address + user agent + session ID for uniqueness
    ip_address = request.META.get('REMOTE_ADDR', '')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # Get or create session ID
    if 'viewer_id' not in request.session:
        request.session['viewer_id'] = str(uuid.uuid4())
        request.session.modified = True
    
    session_id = request.session['viewer_id']
    
    # Create a unique fingerprint for this viewer
    fingerprint_string = f"{ip_address}{user_agent}{session_id}"
    viewer_hash = hashlib.md5(fingerprint_string.encode()).hexdigest()
    
    # Check if this viewer already liked this post
    existing_like = Review.objects.filter(
        bible_post=bible_post, 
        reviewer_id=viewer_hash
    ).first()
    
    if existing_like:
        # Viewer already liked this post - show current count
        return HttpResponse(f'''
            <button class="like-btn text-green-600 cursor-default flex items-center space-x-1" disabled>
                <i class="fas fa-heart"></i>
                <span>{bible_post.reviews}</span>
            </button>
        ''')
    else:
        # First time liking - add the like
        Review.objects.create(
            bible_post=bible_post,
            reviewer_id=viewer_hash
        )
        
        # Update like count
        bible_post.reviews += 1
        bible_post.save()
        
        return HttpResponse(f'''
            <button class="like-btn text-green-600 cursor-default flex items-center space-x-1" disabled>
                <i class="fas fa-heart"></i>
                <span>{bible_post.reviews}</span>
            </button>
        ''')