
# from os import name
# from unicodedata import category
from urllib import request
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Payment, Post, Image, Mission, Board
from datetime import time
import yagmail
from django.contrib import messages
# from decouple import config
from . import forms
from django.conf import settings
from .verify import Payment_session
import re
import secrets
from .forms import PaymentForm, CommentForm
from .paystack import PayStack
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

sender_email = settings.SENDER_EMAIL
sender_password = settings.SENDER_PASSWORD


def validate_input(*args):
        check_against = re.compile(r'[a-zA-Z0-9 ]*$')
        false_arr=[]
        true_arr=[]
        for val in args:
            if check_against.match(val):
                    true_arr.append(val)
                    # print(true_arr)
            else:
                    false_arr.append(val)
                    # print(false_arr)
        if len(false_arr) > 0:
                return False
        return True

def home(request):
    board = Board.objects.all()
    template = 'home.html'
    
    if request.method == "POST":
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']
        subject = 'testing my contact page'
        
        yag = yagmail.SMTP(user=sender_email, password=sender_password)
        
        yag.send(
            #  message_name,
             contents = message,
             subject = subject,
             to = message_email,
            #  to = ['okeke98@gmail.com']
            
        )
        
        context = {'board':board, 'message_name':message_name}
        return render(request, template, context)
    else:
        context = {'board':board}
        return render(request, template, context)
    

    

def about(request):
    template = 'about.html'
    return render(request, template)  

# def categories(request):
#     category = Category.objects.all()
#     template = 'mission-fields.html'
#     return render(request, template, {'category':category})

def mission_fields(request):
    mission_fields = Mission.objects.all()
    # print(mission_fields)
    template = 'mission-fields.html'
    return render(request, template, {'mission_fields':mission_fields})

def mission_fields_detail(request, slug):
    try:
        mission = Mission.objects.get(slug=slug)
        images = Image.objects.filter(mission = mission).order_by('-date_created')
    except:
        print('error')
    context = {'mission':mission, 'images':images}
    return render(request, 'mission-fields_detail.html', context)

# def search_mission(request):
    # if request.method == "POST":
    #     searched = request.POST['searched']
    #     missions = Mission.objects.filter(name__contains=searched)
    #     template = 'search_mission.html'
    #     context = {'searched':searched, 'missions':missions}
    #     return render(request, template, context)
    # else:
    #     return render(request, template,)

def post_list(request):
    posts = Post.published.all()
    # paginator = Paginator(object_list=3) 
    # page = request.GET.get('page')
    # try:
    #     posts = paginator.page(page)
    # except  PageNotAnInteger:
    #     posts = paginator.page(1)
    # except EmptyPage:
    #     posts = paginator.page(paginator.num_pages)
    template = 'post/sol-blog.html'
    return render(request, template, {'posts': posts})
    # return render(request, template, { 'page':page,'posts': posts})

def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    comments = post.comments.filter(active=True)
    
    new_comment = None
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            name = comment_form.cleaned_data['name']
            print(name)
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            print(new_comment.post)
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
            
    context = {'post':post, 
               'comments':comments,
               'new_comment':new_comment,
               'comment_form': comment_form}
    
    template = 'post/sol-blog_detail.html'
    
    return render(request, template, context)

def initiate_payment(request: HttpRequest) -> HttpResponse:
    payment = Payment_session(request)
    payment_form = PaymentForm(request.POST)
    if payment_form.is_valid():
        # get_info = request.POST
        name = payment_form.cleaned_data['name']
        email = payment_form.cleaned_data['email']
        phone_number = str(payment_form.cleaned_data['phone_number'])
        amount = str(payment_form.cleaned_data['amount'])
        village = str(payment_form.cleaned_data['village'])
        description = str(payment_form.cleaned_data['description'])
        ref = secrets.token_urlsafe(50)
        result = {'name':name,
                  'email':email, 
                  'phone_number':phone_number, 
                  'amount':amount,
                  'ref':ref,
                  'village':village,
                  'description':description,
                  }
        if validate_input(name, amount, phone_number) == True: 
            form_result = result
            payment.add(form_result)
            retrieve_form = payment.retrieve()
            # print(retrieve_form)
            email = retrieve_form[1]
            # print(email)
            name = retrieve_form[0]
            amount = retrieve_form[3]
            amount_value = int(amount)*100
            reference = retrieve_form[4]
            village = retrieve_form[5]
            # print(reference)
            context ={'email':email, 
                        'name':name,
                        'amount':amount, 
                        'amount_value':amount_value,
                        'reference':reference, 
                        'village':village,
                        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY}
            return render(request, 'payment/make_payment.html', context)
    else:
        payment_form = forms.PaymentForm()    
    return render(request, 'payment/initiate_payment.html', {'payment_form': payment_form})

def verify_payment(request: HttpRequest, ref:str):
    # print(ref)
    payment = Payment_session(request)
    ref_exists = payment.retrieve()
    if ref_exists:
        ref_exists[4] = ref
        verified = payment.verify_pay()
        if verified:
            payment.clear()
            messages.success(request, "Donation Successfull.")
            return redirect('home')
    else:
        payment.clear()
        messages.error(request, "Donation Failed.")
    return redirect('initiate_payment')





