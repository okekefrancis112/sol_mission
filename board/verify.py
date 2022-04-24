from .paystack import PayStack
from django.conf import settings
from .models import Payment

class Payment_session(object):
    
    def __init__(self, request):
        self.session = request.session
        payment_form = self.session.get(settings.PAYMENT_SESSION_ID)
        
        if not payment_form:
            payment_form = self.session[settings.PAYMENT_SESSION_ID] = {}
            
        self.payment_form = payment_form
        
    def add(self, form = {}, update_form = False):
        # print(form)
        if 'payment_form' not in self.payment_form:
            self.payment_form['payment_form'] = form
            
        if update_form:
            self.payment_form['payment_form'] = form
        else:
            self.payment_form['payment_form'] = form
        self.save()
        # print(self.payment_form)
        
    def save(self):
        self.session.modified = True
        
    def clear(self):
        del self.session[settings.PAYMENT_SESSION_ID]
        self.save
        
    def retrieve(self):
        forms = self.session.get('payment_form')
        for key,value in forms.items():
            lst = list(value.values())[0:7]
            # print(lst)
        # res = lst
        # print(res)
            return lst
            
       
    def verify_pay(self):
        paystack = PayStack()
        pay = self.retrieve()
        # print(pay)
        name = pay[0]
        email = pay[1]
        phone_number = pay[2]
        ref = pay[4]
        amount = int(pay[3])
        village = pay[5]
        description = pay[6]
        status, result = paystack.verify_payment(amount, ref)
        if status: 
            res = result['requested_amount'] 
            # print(res)
            re = int(res / 100)
            # print(type(re))
            # print(re)
            if re == amount:
                # print('true')
                save_payment_details = Payment(name=name, 
                                               phone_number=phone_number, 
                                               village=village, amount=amount, 
                                               ref=ref, 
                                               email=email, 
                                               description=description,
                                               )
                save_payment_details.save()
                return True
        return False







