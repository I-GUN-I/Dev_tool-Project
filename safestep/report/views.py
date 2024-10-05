from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.db.models import Value, Count, F,Sum
from django.db.models.functions import Concat
from datetime import datetime
from report.forms import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import *
from django.contrib.contenttypes.models import ContentType
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from twilio.base.exceptions import TwilioException
from twilio.rest import Client
from report.models import *


class Report(View):
    def get(self, request):
        return render(request,'index.html') 
    
class ReportAction(LoginRequiredMixin, View):
    login_url = '/login/'
    api = TwilioAPI.objects.first()
    def post(self, request):
        api = TwilioAPI.objects.first()
        account_sid = api.account_sid
        auth_token = api.auth_token
        client = Client(account_sid, auth_token)

        to_number = request.user.customer.phone
        from_number = api.tel

        try:
            message = client.messages.create(
                body="ตรวจพบการล้ม",
                from_=from_number,
                to=to_number
            )

            return HttpResponse(f"SMS sent with SID: {message.sid}")  # Return the SID of the sent message
        except TwilioException as e:
            return HttpResponse(f"Failed to send SMS: {str(e)}", status=500)


class LoginView(View):
    
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'authentication/login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)

            if user is not None:
                login(request,user)
                return redirect('index')
            else:
                messages.error(request,'invalid username')
        else:
            messages.error(request,'invalid username')
        return render(request,'authentication/login.html', {'form':form})
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/login/')
    
class RegisterView(View):
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            my_user = form.save()
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            Customer.objects.create(
                user = my_user,
                phone = phone,
                address = address,
                contact=None
            )
            messages.success(request, 'Account created successfully')
            return redirect('login') 
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'authentication/register.html', {'form': form}) 

    def get(self, request):
        form = CustomUserCreationForm()
        context = {
            'form': form
        }
        return render(request, 'authentication/register.html', context)
    
class UserProfileView(View):
    def get(self, request,user_id):
        customer = Customer.objects.get(pk=user_id)
        context = {
            'customer' : customer
        }
        # เรนเดอร์เทมเพลตพร้อมกับส่ง context ไป
        return render(request, 'profile.html',context)
    
