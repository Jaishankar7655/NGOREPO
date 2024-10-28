from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'), 
    path('about/', views.about, name='about'),  # about us  route
    path('services/', views.service, name='services'),  # Services route
    path('donation/', views.donate, name='donate'),  # Services route
    path('gallery/', views.gallery, name='gallery'),  #gallery
    path('admin/', admin.site.urls),  # Admin route
    path('testimonials/', views.testimonial_list, name='testimonial_list'),   # Testimonial list
    path('registration/', views.register, name='register'),   # Registration route
    path('userdashboard'  , views.dashboard , name='dashboard'),   # Registration route
    path('IDcard'  , views.idcard , name='card'),   # Registration route
    path('profile'  , views.profile , name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),   # Registration route
    path('certificate/', views.certificate, name='certificate'),   # Registration route
    path('appointment/', views.appointment, name='appointment'),   # Registration route
    path('certificate_list' , views.certificate_list, name='certificate_list'),
    path('servicedetails/' , views.servicedetails, name='servicedetails'),
    path('ApplicationForAppointment/' , views.apl, name='apl'), #
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)