from django.contrib import admin
from .models import YouTubeTestimonial
admin.site.register(YouTubeTestimonial)


from .models import Image
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')

from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'mobile_number', 'registration_date', 'letter_number')
    search_fields = ('name', 'mobile_number', 'aadhaar_number', 'letter_number')
    list_filter = ('position', 'registration_date')
    date_hierarchy = 'registration_date'
    
    fieldsets = (
        ('व्यक्तिगत जानकारी', {
            'fields': ('name', 'guru_father_husband', 'address', 'mobile_number', 'aadhaar_number', 'profile_picture')
        }),
        ('नियुक्ति विवरण', {
            'fields': ('position', 'registration_date', 'letter_number')
        }),
    )

# certificates/admin.py


# admin.py
# admin.py
from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_number', 'letter_number', 'date')
    search_fields = ('name', 'mobile_number', 'letter_number')











