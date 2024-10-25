from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password, check_password
import mysql.connector
from App.models import Image, YouTubeTestimonial
from django.utils.translation import gettext as _

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
def certificate(request):
    return render(request, 'Certificate.html')


# views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from App.models import Appointment

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




# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from App.models import Donation
import uuid
import json
import base64
import hashlib
import requests

def donation_page(request):
    return render(request, 'donations/donation.html')

@csrf_protect
def process_donation(request):
    if request.method == 'POST':
        try:
            # Create donation record
            donation = Donation.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                mobile=request.POST.get('mobile'),
                amount=float(request.POST.get('amount')),
                address=request.POST.get('address'),
                bank_name=request.POST.get('bank_name'),
                account_number=request.POST.get('account_number'),
                transaction_id=f"TXN_{uuid.uuid4().hex[:20]}",
                merchant_transaction_id=f"MERCH_{uuid.uuid4().hex[:20]}",
                payment_status='PENDING'
            )

            # PhonePe payment integration
            phonepe = PhonePePayment()
            payload = phonepe.generate_payload(donation)
            
            # Make request to PhonePe
            response = requests.post(
                phonepe.api_endpoint,
                json={"request": payload['payload']},
                headers={
                    'Content-Type': 'application/json',
                    'X-VERIFY': payload['hash']
                }
            )
            
            response_data = response.json()
            
            if response_data.get('success'):
                # Update donation with payment details
                donation.payment_response = response_data
                donation.save()
                
                return JsonResponse({
                    'success': True,
                    'redirect_url': response_data['data']['instrumentResponse']['redirectInfo']['url']
                })
            else:
                raise Exception(response_data.get('message', 'Payment initiation failed'))

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)

class PhonePePayment:
    def __init__(self):
        self.merchant_id = settings.PHONEPE_MERCHANT_ID
        self.salt_key = settings.PHONEPE_SALT_KEY
        self.salt_index = settings.PHONEPE_SALT_INDEX
        
        if settings.DEBUG:
            self.api_endpoint = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay"
        else:
            self.api_endpoint = "https://api.phonepe.com/apis/hermes/pg/v1/pay"

    def generate_payload(self, donation):
        payload = {
            "merchantId": self.merchant_id,
            "merchantTransactionId": donation.merchant_transaction_id,
            "merchantUserId": f"MUID_{donation.id}",
            "amount": int(donation.amount * 100),  # Convert to paisa
            "redirectUrl": f"{settings.SITE_URL}/payment/callback/",
            "redirectMode": "POST",
            "callbackUrl": f"{settings.SITE_URL}/api/payment/callback/",
            "paymentInstrument": {
                "type": "PAY_PAGE"
            }
        }
        
        base64_payload = base64.b64encode(json.dumps(payload).encode()).decode()
        
        # Generate hash
        string_to_hash = base64_payload + "/pg/v1/pay" + self.salt_key
        sha256_hash = hashlib.sha256(string_to_hash.encode('utf-8')).hexdigest()
        hash_value = f"{sha256_hash}###{self.salt_index}"
        
        return {
            'payload': base64_payload,
            'hash': hash_value
        }