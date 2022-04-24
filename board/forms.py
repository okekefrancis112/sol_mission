from django import forms
from .models import Mission, Payment, Comment

class PaymentForm(forms.ModelForm):
    village = forms.ModelChoiceField(queryset=Mission.objects.all(), empty_label="Select a Community", label='')    
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name'}), label='')
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}), label='')
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Phone number'}), label='')
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Description'}), label='')
    amount = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Amount'}), label='')
        
    class Meta:
        model = Payment
        fields = ("name", "email", "phone_number", "description", "village", "amount")
        
class CommentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your name'}))
    body = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Post a Comment'}))
    class Meta:
        model = Comment
        fields = ('name', 'body')
        