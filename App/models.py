from django.db import models


from django.utils import timezone

class Image(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='gallery/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
    


class YouTubeTestimonial(models.Model):
    title = models.CharField(max_length=200)
    youtube_link = models.URLField()
    testimonial_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def youtube_video_id(self):
        # Extract video ID from YouTube URL
        if "youtu.be" in self.youtube_link:
            return self.youtube_link.split("/")[-1]
        elif "youtube.com" in self.youtube_link:
            return self.youtube_link.split("v=")[-1].split("&")[0]
        return None


from django.db import models

class Register(models.Model):
    member_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='photos/')
    password = models.CharField(max_length=255)
    registration_date = models.DateTimeField(auto_now_add=True)



# models.py
from django.db import models
from django.utils import timezone

class Appointment(models.Model):
    name = models.CharField(max_length=200, verbose_name="नाम")
    guru_father_husband = models.CharField(max_length=200, verbose_name="गुरु/पिता/पति")
    address = models.TextField(verbose_name="पता")
    mobile_number = models.CharField(max_length=15, verbose_name="मोबाइल नंबर")
    aadhaar_number = models.CharField(max_length=12, verbose_name="आधार नंबर")
    position = models.CharField(max_length=100, verbose_name="पद")
    profile_picture = models.ImageField(upload_to='profile_pictures/', verbose_name="प्रोफाइल पिक्चर")
    registration_date = models.DateField(default=timezone.now, verbose_name="पंजीकरण दिनांक")
    letter_number = models.CharField(max_length=50, unique=True, verbose_name="पत्र क्रमांक")

    def __str__(self):
        return f"{self.name} - {self.position}"

    class Meta:
        verbose_name = "नियुक्ति पत्र"
        verbose_name_plural = "नियुक्ति पत्र"

# admin.py




# views.py
from django.shortcuts import render, get_object_or_404
from .models import Appointment

def appointment(request):
    if request.method == 'GET' and 'id' in request.GET:
        appointment = get_object_or_404(Appointment, id=request.GET['id'])
        return render(request, 'appointment.html', {'appointment': appointment})
    return render(request, 'appointment_list.html', {'appointments': Appointment.objects.all()})








# certificat/model


# models.py
from django.db import models

class Certificate(models.Model):
    name = models.CharField(max_length=100, verbose_name="नाम")
    guardian = models.CharField(max_length=100, verbose_name="गुरु/पिता/पति")
    area = models.CharField(max_length=200, verbose_name="पता")
    workarea = models.CharField(max_length=200, verbose_name="कार्य क्षेत्र")
    field = models.CharField(max_length=200, verbose_name="क्षेत्र")
    welfare_activity = models.CharField(max_length=200, verbose_name="कल्याण कार्य")
    date = models.DateField(verbose_name="तारीख")
    letter_number = models.CharField(max_length=50, verbose_name="पत्र क्रमांक")
    mobile_number = models.CharField(max_length=15, unique=True, verbose_name="मोबाइल नंबर")
    
    def __str__(self):
        return self.name
