# lfc_teens/admin.py
from django.contrib import admin
from .models import *

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active']
    list_editable = ['is_active']
    search_fields = ['title', 'subtitle']

@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'position']

@admin.register(BiblePost)
class BiblePostAdmin(admin.ModelAdmin):
    list_display = ['scriptures', 'likes', 'created_at', 'is_active']
    list_editable = ['is_active']
    search_fields = ['scriptures', 'message']

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['topic', 'date', 'is_active']
    list_editable = ['is_active']
    list_filter = ['date', 'is_active']
    search_fields = ['topic', 'announcement']

@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    list_display = ['testifier', 'topic', 'date', 'is_approved']
    list_editable = ['is_approved']
    list_filter = ['is_approved', 'date']
    search_fields = ['testifier', 'topic', 'testimony']

@admin.register(MinistryUnit)
class MinistryUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'leader', 'leader_whatsapp', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'leader', 'duty']

@admin.register(Belief)
class BeliefAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'detail']

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['church_name', 'phone_number', 'email']
    
    def has_add_permission(self, request):
        # Allow only one contact info entry
        return not ContactInfo.objects.exists()