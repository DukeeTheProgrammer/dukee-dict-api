from django.shortcuts import render
from django.contrib.auth.models import User
import random
from .dict_tools import get_word
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from dict_auth.models import Profile
from django.http import JsonResponse






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

@method_decorator(csrf_exempt, name='dispatch')
class SearchWord(View):
    def get(self, request, word):
        auth = request.headers.get("X-Authorization")
        token = request.headers.get("X-token")


        pro = Profile.objects.filter(token=token,api_key=auth).first()
        user = pro.user if pro else "Anonymous"


        if not pro:
            return JsonResponse({
                "error":True,
                "success":False,
                "message":"No user seems to be Authenticated Due to invalid Token or auth. Please verify your headers"
                })
        else:
            if not user and not pro.api_key:
                return JsonResponse({
                    "error":True,
                    "success":False,
                    "message":"Authentication Failed, Please make sure your sending the right API key wih your request headers"
                    })
            elif not pro.token:
                return JsonResponse({
                    "error":True,
                    "success":False,
                    "message":"Token is invalid For this request. Go to your dashboard and make sure your using the right token"
                    })

            else:
                if not word:
                    return JsonResponse({
                        "error":True,
                        "success":False,
                        "message":"Make sure your word parameter is not empty"
                        })
                else:
                    request.session["word"] = word
                    result = get_word(word)

                    return JsonResponse({
                        "error":False,
                        "success":True,
                        "message":result,
                        "info":"Please Read user guide for more info"
                        })

    def post(self, request, word):
        return JsonResponse({
            "error":True,
            "success":False,
            "message":"POST is not yet avaiable for this endpoint."
            })
