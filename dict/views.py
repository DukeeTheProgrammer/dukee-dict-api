from django.shortcuts import render
from django.contrib.auth.models import User
import random






def GetWord(request):
    pass



def DashBoard(request):
    if request.method == "GET":

        user = request.user

        requests = user.profile.logs.requests
        percent = random.uniform(0,100)
        percent2 = random.uniform(1,100)
        ip = user.profile.logs.ip 
        api_health = random.uniform(80,100)

        return render(request, "dashboard.html",
                      {
                          "requests":requests,
                          "percent":percent,
                          "percent2":percent2,
                          "ip":ip,
                          "api_health":api_health
                          })
    else:
        pass


def api(request):
    user = request.user 

    try:
        api_key = request.user.profile.api_key
        token = request.user.profile.api_key
        date = request.user.date_joined

        return render(request, "api.html", {"token":token, "api_key":api_key, "date":date})
    except Exception as e:
        return render(request, "api.html", {"token":"Error Getting Token", "api_key":'Error Getting API key', "date":"Error getting date"})



def token(request):
    user = request.user

    try:
        token = request.user.profile.token

        return render(request,"token.html", {"token":token})
    except Exception as e:
        return render(request, "token.html", {"token":"Token Generation Failed"})
