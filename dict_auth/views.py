from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile, Log
from django.http import JsonResponse
from django.views import View 
from django.contrib.auth.hashers import check_password
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
                profile=new_profile,
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
        pass


class Logout(View):
    def get(self, request):
        try:
            request.session.flush()
            return render(request, "login.html")
        except Exception as e:
            return render(request, "login.html")

    def post(self, request):
        return render(request, "login.html")



class ForgotPassword(View):
    pass
