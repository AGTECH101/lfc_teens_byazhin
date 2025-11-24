# lfc_teens/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
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
        'contact_info': contact_info,
    }
    return render(request, 'index.html', context)

def like_bible_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('pk')
        try:
            post = BiblePost.objects.get(id=post_id)
            post.likes += 1
            post.save()
            return JsonResponse({'success': True, 'likes': post.likes})
        except BiblePost.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})