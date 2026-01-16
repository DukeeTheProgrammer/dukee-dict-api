from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile, Log
from django.http import JsonResponse
from django.views import View 
from django.contrib.auth.hashers import check_password
from django.utils import timezone
import random, string

from .tools import(
        api_key,
        generate_token,
        )
from django.contrib.auth import (
        login,
        logout,
        )


class Signup(View):
    def get(self, request):
        return render(request, "signup.html")
    def post(self, request):
        fullname = request.POST.get('fullname')
        email = request.POST.get("email")
        password = request.POST.get("password")

        #validates if the above credential is valid 

        if not email or not password:
            return JsonResponse({"status":{
                "error":True,
                "success":False,
                "message": "Email and Password Fields are required"}, "from":"DukeeTheProgrammer"
                                 })

        #now check the credentials against the data base

        user = User.objects.filter(email=email).first()

        if user:
            return JsonResponse({"status": {
                "error":True,
                "success":False,
                "message":"Email already exists in the database, Try logging in instead if this is your account."
                }, "from":"DukeeTheProgrammer"
                                 })
        #creates new user if the checked email not found
        api = api_key()
        aplh=string.ascii_letters
        username = random.sample(aplh, k=10)
        new_user = User.objects.create_user(
                username=username,
                first_name=fullname,
                email=email,
                password=password
                )
        new_user.save()

        tok = generate_token()
        new_profile=Profile.objects.create(
                user=new_user,
                api_enabled=True,
                api_key=api,
                token=tok
                )
        ip_addr = request.META.get("REMOTE_ADDR")
        new_profile.save()
        new_log = Log.objects.create(
                user=new_profile,
                ip=ip_addr
                )
        new_log.save()

        return JsonResponse({
                "status": {
                    "error":False,
                    "success":True,
                    "message":"Account has been crreated Successfully"
                    }, "from":"DukeeTheProgrammer"
                })


class Login(View):
    def get(self, request):
        return render(request, "login.html")
    def post(self,request):

        #get online credentials...

        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            return JsonResponse({"status":{
                    "error":True,
                    "success":False,
                    "message": "Email and Password Fields are required"}, "from":"DukeeTheProgrammer"
                                 })
        user = User.objects.filter(email=email).first()
        if user:
            #check for password

            if check_password(password, user.password):
                user.logged_in = True
                login(request, user)
                user.save()
                return JsonResponse({
                    "status":{
                        "error":False,
                        "success":True,
                        "message":"Login was succesful"
                        }, "from":"DukeeTheProgrammer"
                    })
            else:
                return JsonResponse({
                    "status": {
                        "error":True,
                        "success":False,
                        "message":"Wrong Password Entered"
                        }, "from":"DukeeTheProgrammer"
                    })
        else:
            #when user doesnt exists
            return JsonResponse({
                "status": {
                    "error":True,
                    "success":False,
                    "message":"Invalid Username and password"
                    }, "from":"DukeeTheProgrammer"
                })



class WelcomePage(View):
    def get(self, request):
        return render(request, "welcome.html")

    def post(self, request):
        return render(request, "error.html", {
            "error_code":400,
            "error_title":"Wrong Method Sent To this Server",
            "message":"You have sent A Post request to this server but it is not accepted",
            "timestamp":timezone.now
            })


class GetDictWord(View):
    def get(self, request):
        return render(request, "dashboard.html")
    def post(self, request):
        return render(request, "error.html", {
            "error_code":400,
            "error_title":"Wrong Method Sent To this Server",
            "message":"You have sent A Post request to this server but it is not accepted",
            "timestamp":timezone.now
            })




class Logout(View):
    def get(self,request):
        user = request.user
        try:
            if request.session:
                request.session.flush()
                return render(request, "login.html")
            return render(request, 'login.html')
        except Exception as e:
            return render(request, "error.html", {
                "error_code":500,
                "message": f"Could not Log you out. This Could Happen if your session has expired. You can try logging in again to resolve the issue.",
                "error_title": "Logout Misdirection",
                "timestamp" :timezone.now}
                          )
    def post(self, request):
        
        return render(request, "error.html", {
            "error_code":500,
            "error_title":"Wrong Method Sent To this Server",
            "message":"You have sent A Post request to this server but it is not accepted",
            "timestamp":timezone.now
            })
