import json
import base64
import hashlib
import requests
from django.conf import settings
from decimal import Decimal
from App.models import Donor, DonationTransaction

class PhonePePayment:
    def __init__(self):
        self.MERCHANT_ID = settings.PHONEPE_MERCHANT_ID
        self.SALT_KEY = settings.PHONEPE_SALT_KEY
        self.SALT_INDEX = settings.PHONEPE_SALT_INDEX
        self.ENV = 'UAT' if settings.DEBUG else 'PROD'
        self.API_URL = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay" if settings.DEBUG else "https://api.phonepe.com/apis/hermes/pg/v1/pay"

    def create_donation_record(self, data):
        # Create or update donor
        donor, created = Donor.objects.get_or_create(
            email=data['email'],
            defaults={
                'name': data['name'],
                'mobile': data['mobile'],
                'address': data['address']
            }
        )

        # Create donation transaction
        donation = DonationTransaction.objects.create(
            donor=donor,
            amount=data['amount'],
            bank_name=data['bank_name'],
            account_number=data['account_number']
        )

        return donation

    def generate_payload(self, donation):
        payload = {
            "merchantId": self.MERCHANT_ID,
            "merchantTransactionId": str(donation.id),
            "merchantUserId": f"MUID{donation.donor.id}",
            "amount": int(float(donation.amount) * 100),
            "redirectUrl": f"{settings.SITE_URL}/payment/callback/",
            "redirectMode": "POST",
            "callbackUrl": f"{settings.SITE_URL}/payment/callback/",
            "paymentInstrument": {
                "type": "PAY_PAGE"
            }
        }
        return payload

    def generate_checksum(self, payload):
        payload_base64 = base64.b64encode(json.dumps(payload).encode()).decode()
        string = f"{payload_base64}/pg/v1/pay{self.SALT_KEY}"
        sha256_hash = hashlib.sha256(string.encode()).hexdigest()
        checksum = f"{sha256_hash}###{self.SALT_INDEX}"
        return payload_base64, checksum

    def initiate_payment(self, form_data):
        try:
            # Create donation record
            donation = self.create_donation_record(form_data)
            
            # Generate payment payload
            payload = self.generate_payload(donation)
            payload_base64, checksum = self.generate_checksum(payload)

            headers = {
                "Content-Type": "application/json",
                "X-VERIFY": checksum
            }

            request_data = {
                "request": payload_base64
            }

            response = requests.post(
                self.API_URL,
                json=request_data,
                headers=headers
            )

            return response.json(), donation.id

        except Exception as e:
            return {"error": str(e)}, None