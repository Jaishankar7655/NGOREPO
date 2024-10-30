from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password, check_password
import mysql.connector
from App.models import Image, YouTubeTestimonial
from django.utils.translation import gettext as _
from functools import wraps
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Q



# Database connection
db = mysql.connector.connect(
    host='localhost',
    user='u834728860_ngo',
    passwd='Akhada@2024',
    database='u834728860_akhada_ngo'
)
cr = db.cursor()
# Login Required Decorator
def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'username' not in request.session:
            # Store the intended URL in session
            request.session['next'] = request.get_full_path()
            messages.warning(request, 'Please login to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Check if user is already logged in
def check_logged_in(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'username' in request.session:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Public views that don't require login
def home(request):
    return render(request, 'home.html')

def nav(request):
    return render(request, 'Nav.html')

def header(request):
    return render(request, 'Header.html')

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'services.html')

def donate(request):
    return render(request, 'donation.html')

def gallery(request):
    images = Image.objects.all().order_by('-created_at')
    return render(request, 'gallery.html', {'images': images})

def testimonial_list(request):
    testimonials = YouTubeTestimonial.objects.all().order_by('-created_at')
    return render(request, 'testimonials.html', {'testimonials': testimonials})

def apl(request):
    return render(request, 'apl.html')

def contact(request):
    return render(request, 'contact.html')

# Authentication views
@check_logged_in
def register(request):
    if request.method == 'POST':
        firstname = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        username = request.POST.get('username')
        password = request.POST.get('password')
        mother_name = request.POST.get('motherName')
        father_name = request.POST.get('fatherName')
        gender = request.POST.get('gender')
        street = request.POST.get('street')
        city = request.POST.get('city')
        postal_code = request.POST.get('postalCode')
        state = request.POST.get('state')
        country = request.POST.get('country')
        photo = request.FILES.get('photo')

        if photo:
            fs = FileSystemStorage()
            filename = fs.save(photo.name, photo)
            photo_url = fs.url(filename)
        else:
            photo_url = None

        try:
            insert_query = """INSERT INTO register 
                              (name, email, mobile, username, password, mother_name, 
                               father_name, gender, street, city, postal_code, state, 
                               country, photo)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            hashed_password = make_password(password)
            cr.execute(insert_query, (
                firstname, email, mobile, username, hashed_password, 
                mother_name, father_name, gender, street, city, 
                postal_code, state, country, photo_url
            ))
            db.commit()

            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')

        except mysql.connector.Error as err:
            messages.error(request, f"Error: {err}")
            db.rollback()

    return render(request, 'register.html')

@check_logged_in
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        try:
            cr.execute("SELECT * FROM register WHERE username = %s", (username,))
            user = cr.fetchone()

            if user:
                hashed_password = user[14]
                if check_password(password, hashed_password):
                    # Set session
                    request.session['username'] = username
                    
                    # If remember me is checked, set session expiry to 30 days
                    if remember_me:
                        request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days in seconds
                    else:
                        request.session.set_expiry(0)  # Session expires when browser closes
                    
                    # Redirect to the intended URL if it exists
                    next_url = request.session.get('next', 'dashboard')
                    if 'next' in request.session:
                        del request.session['next']
                    return redirect(next_url)
                else:
                    messages.error(request, 'Invalid password. Please try again.')
            else:
                messages.error(request, 'Username does not exist.')

        except mysql.connector.Error as err:
            messages.error(request, f"Database error: {err}")

    return render(request, 'login.html')

# Protected views that require login
@login_required
def dashboard(request):
    username = request.session.get('username')
    cr.execute("SELECT * FROM register WHERE username = %s", (username,))
    user = cr.fetchone()

    if user:
        context = {
            'member_id': user[0],
            'username': user[1],
            'email': user[2],
            'name': user[3],
            'mother_name': user[4],
            'father_name': user[5],
            'gender': user[6],
            'address': f"{user[7]}, {user[8]}, {user[9]}, {user[10]}, {user[11]}",
            'mobile': user[12],
            'registration_date': user[15],
            'photo': user[13]
        }
        return render(request, 'dashboard.html', context)

    return redirect('login')

@login_required
def idcard(request):
    username = request.session.get('username')
    cr.execute("SELECT * FROM register WHERE username = %s", (username,))
    user = cr.fetchone()

    if user:
        context = {
            'name': user[3],
            'father_name': user[5],
            'mother_name': user[4],
            'registration_date': user[15],
            'address': f"{user[7]}, {user[8]}, {user[9]}, {user[10]}, {user[11]}",
            'mobile': user[12],
            'photo': user[13],
            'school': _("अघोर अखाड़ा ज्योतिष पीठ"),
            'school_address': _("उज्जैन मध्यप्रदेश"),
            'school_phone': _("फोन: 9691147442")
        }
        return render(request, 'card.html', context)

    return redirect('login')

@login_required
def profile(request):
    username = request.session.get('username')
    cr.execute("SELECT * FROM register WHERE username = %s", (username,))
    user = cr.fetchone()
    
    if user:
        context = {
            'username': user[1],
            'name': user[3],
            'email': user[2],
            'mobile': user[12],
            'father_name': user[5],
            'mother_name': user[4],
            'gender': user[6],
            'address': f"{user[7]}, {user[8]}, {user[9]}, {user[10]}, {user[11]}",
            'registration_date': user[15],
            'photo': user[13]
        }
        return render(request, 'profile.html', context)

    return redirect('login')

@login_required
def edit_profile(request):
    username = request.session.get('username')
    if request.method == 'POST':
        cr.execute("SELECT * FROM register WHERE username = %s", (username,))
        user = cr.fetchone()

        if user:
            name = request.POST.get('name', user[3])
            email = request.POST.get('email', user[2])
            mobile = request.POST.get('mobile', user[12])
            mother_name = request.POST.get('mother_name', user[4])
            father_name = request.POST.get('father_name', user[5])
            gender = request.POST.get('gender', user[6])
            street = request.POST.get('street', user[7])
            city = request.POST.get('city', user[8])
            postal_code = request.POST.get('postal_code', user[9])
            state = request.POST.get('state', user[10])
            country = request.POST.get('country', user[11])

            photo = request.FILES.get('photo')
            if photo:
                fs = FileSystemStorage()
                filename = fs.save(photo.name, photo)
                photo_url = fs.url(filename)
            else:
                photo_url = user[13]

            try:
                update_query = """UPDATE register SET 
                                  name=%s, email=%s, mobile=%s, mother_name=%s, 
                                  father_name=%s, gender=%s, street=%s, city=%s, 
                                  postal_code=%s, state=%s, country=%s, photo=%s
                                  WHERE username=%s"""
                cr.execute(update_query, (name, email, mobile, mother_name, 
                                          father_name, gender, street, city, 
                                          postal_code, state, country, photo_url, username))
                db.commit()
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
            except mysql.connector.Error as err:
                messages.error(request, f"Error updating profile: {err}")
                db.rollback()

    cr.execute("SELECT * FROM register WHERE username = %s", (username,))
    user = cr.fetchone()
    if user:
        context = {
            'name': user[3],
            'email': user[2],
            'mobile': user[12],
            'mother_name': user[4],
            'father_name': user[5],
            'gender': user[6],
            'street': user[7],
            'city': user[8],
            'postal_code': user[9],
            'state': user[10],
            'country': user[11],
            'photo': user[13]
        }
        return render(request, 'edit_profile.html', context)

    return redirect('login')





from django.shortcuts import render, redirect
from django.db.models import Q
from App.models import Certificate

def certificate_list(request):
    certificates = []
    search_query = request.GET.get('search', '')
    
    if search_query:
        # Search only if there's a query
        certificates = Certificate.objects.filter(
            mobile_number__icontains=search_query
        )
    
    context = {
        'certificates': certificates,
        'search_query': search_query
    }
    return render(request, 'certificate_list.html', context)

def certificate(request):
    mobile_number = request.GET.get('mobile_number')
    try:
        certificate = Certificate.objects.get(mobile_number=mobile_number)
        return render(request, 'certificate.html', {'certificate': certificate})
    except Certificate.DoesNotExist:
        return redirect('certificate_list')





from App.models import Appointment
@login_required
def appointment(request):
    search_query = request.GET.get('search', '')
    appointment_id = request.GET.get('id')

    # If an ID is provided, show the specific appointment
    if appointment_id:
        appointment = get_object_or_404(Appointment, id=appointment_id)
        return render(request, 'appointment.html', {'appointment': appointment})

    # If there's a search query, filter appointments
    if search_query:
        appointments = Appointment.objects.filter(
            Q(mobile_number__icontains=search_query)
        ).order_by('-registration_date')
    else:
        appointments = []

    return render(request, 'appointment_list.html', {
        'appointments': appointments,
        'search_query': search_query
    })












def servicedetails(request):
    return render(request, 'servicedetails.html')

def logout(request):
    if 'username' in request.session:
        del request.session['username']
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')
def apl(request):
    return render(request, 'Apl.html')