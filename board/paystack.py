from urllib import response
from django.conf import  settings
import requests

class PayStack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = 'https://api.paystack.co'
    def verify_payment(self, ref, amount):
        # print(ref)
        # print(amount)
        path = f'/transaction/verify/{amount}'
        
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            'content-Type': 'application/json',
        }
        
        url = self.base_url + path
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # print(response.status_code)
            response_data = response.json()
            # print(response_data)
            return response_data['status'], response_data['data']
        response_data = response.json()
        # print(response_data)
        return response_data["status"], response_data["message"]