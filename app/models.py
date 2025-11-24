# lfc_teens/models.py
from django.db import models
from cloudinary.models import CloudinaryField

class HeroSlide(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField()
    image = CloudinaryField('hero_image', folder='lfc_teens/hero')
    btn_text = models.CharField(max_length=50, default='Learn More')
    btn_link = models.CharField(max_length=200, default='#')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Leader(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    description = models.TextField()
    image = CloudinaryField('leader_image', folder='lfc_teens/leaders')
    # whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.position}"

class BiblePost(models.Model):
    scriptures = models.CharField(max_length=200)
    message = models.TextField()
    image = CloudinaryField('bible_image', folder='lfc_teens/bible')
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.scriptures

class Announcement(models.Model):
    topic = models.CharField(max_length=200)
    announcement = models.TextField()
    date = models.DateField()
    image = CloudinaryField('announcement_image', folder='lfc_teens/announcements', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic

class Testimony(models.Model):
    testifier = models.CharField(max_length=100)
    topic = models.CharField(max_length=200)
    testimony = models.TextField()
    image = CloudinaryField('testimony_image', folder='lfc_teens/testimonies', null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.testifier} - {self.topic}"

class MinistryUnit(models.Model):
    name = models.CharField(max_length=100)
    duty = models.CharField(max_length=200)
    description = models.TextField()
    leader = models.CharField(max_length=100)
    leader_whatsapp = models.CharField(max_length=20, blank=True, null=True)
    image = CloudinaryField('unit_image', folder='lfc_teens/units')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Belief(models.Model):
    name = models.CharField(max_length=100)
    detail = models.TextField()
    image = CloudinaryField('belief_image', folder='lfc_teens/beliefs')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class ContactInfo(models.Model):
    church_name = models.CharField(max_length=200, default="LFC Teens Byazhin")
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    whatsapp_number = models.CharField(max_length=20)
    service_times = models.TextField(help_text="Enter service times with days and times")
    
    def __str__(self):
        return "Contact Information"

    class Meta:
        verbose_name_plural = "Contact Information"