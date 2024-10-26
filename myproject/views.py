from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password, check_password
import mysql.connector
from App.models import Image, YouTubeTestimonial
from django.utils.translation import gettext as _





# Add this at the top of views.py
from functools import wraps
from django.shortcuts import redirect

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'username' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view




# Database connection
db = mysql.connector.connect(host='localhost', user='root', passwd='', database='ngo')
cr = db.cursor()

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
                              (name, email, mobile, username, password, mother_name, father_name, gender, street, city, postal_code, state, country, photo)
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

def login_view(request):
    if request.session.get('username'):
        return redirect('dashboard')  # Redirect to dashboard if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            cr.execute("SELECT * FROM register WHERE username = %s", (username,))
            user = cr.fetchone()

            if user:
                hashed_password = user[14]
                if check_password(password, hashed_password):
                    messages.success(request, 'Login successful!')
                    request.session['username'] = username
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid password. Please try again.')
            else:
                messages.error(request, 'Username does not exist.')

        except mysql.connector.Error as err:
            messages.error(request, f"Database error: {err}")

    return render(request, 'login.html')

@login_required
def dashboard(request):
    username = request.session.get('username')
    if username:
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
    if username:
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
    if username:
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
    if not username:
        return redirect('login')

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



from django.shortcuts import render, get_object_or_404
from App.models import Certificate
@login_required
def certificate_list(request):
    search_query = request.GET.get('search', '')
    certificates = Certificate.objects.filter(mobile_number__icontains=search_query) if search_query else None
    return render(request, 'certificate_list.html', {'certificates': certificates, 'search_query': search_query})
@login_required
def certificate_detail(request):
    mobile_number = request.GET.get('mobile_number')
    if mobile_number:
        certificate = get_object_or_404(Certificate, mobile_number=mobile_number)
        context = {
            'name': certificate.name,
            'guardian': certificate.guardian,
            'area': certificate.area,
            'workarea': certificate.workarea,
            'field': certificate.field,
            'welfare_activity': certificate.welfare_activity,
            'date': certificate.date,
            'letter_number': certificate.letter_number
        }
        return render(request, 'certificate.html', context)
    return redirect('certificate_list')



# views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from App.models import Appointment
@login_required
def appointment(request):
    search_query = request.GET.get('search', '')  # Get search query (mobile number)
    appointment_id = request.GET.get('id')  # Check if the "view" button is clicked
    
    if appointment_id:
        # Show the specific appointment details in appointment.html
        appointment = get_object_or_404(Appointment, id=appointment_id)
        return render(request, 'appointment.html', {'appointment': appointment})
    
    if search_query:
        # Filter appointments based on mobile number
        appointments = Appointment.objects.filter(
            Q(mobile_number__icontains=search_query)
        ).order_by('-registration_date')
    else:
        # If no search query, return an empty list (hide appointments)
        appointments = []
    
    return render(request, 'appointment_list.html', {
        'appointments': appointments,
        'search_query': search_query
    })


@login_required
# Add a new view for downloading
def appointment_download(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    # Your PDF generation logic here
    return render(request, 'appointment.html', {
        'appointment': appointment,
        'download_mode': True
    })


def servicedetails(request):
    return render(request, 'servicedetails.html')


def logout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('home')








