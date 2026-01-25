from django.shortcuts import render
from django.contrib.auth.models import User
import random
from .dict_tools import get_word
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from dict_auth.models import Profile, Log
from django.http import JsonResponse






def GetWord(request):
    pass



def DashBoard(request):
    if request.method == "GET" or request.method=="POST" or request.method=="OPTIONS":

        user = request.user

        log = Log.objects.filter(profile=user.profile).first()
        requests_made = log.requests
        api_key = user.profile.api_key
        print(f"REQUESTS MADE : {requests_made}")
        percent = random.uniform(0,100)
        percent2 = random.uniform(1,100)
        ip = user.profile.logs.ip 
        api_health = random.uniform(80,100)
        date = user.date_joined

        return render(request, "dashboard.html",
                      {
                          "date":date,
                          "api_key":api_key,
                          "requests_made":requests_made,
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
        try:
            log = Log.objects.filter(profile=pro).first()
            log.requests +=1 
            log.save()
        except Exception as e:
            print(f"Could not Save Log : {e}")


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



from django.shortcuts import render
from datetime import datetime, timedelta
import json

def analytics_dashboard(request):
    context = {
        'total_requests': 1248579,
        'active_users': 2847,
        'total_revenue': 24857,
        'uptime_percentage': 99.92,
        'start_date': '2023-10-01',
        'end_date': '2023-10-26',
        'current_date': datetime.now().strftime('%B %d, %Y'),
        'last_refresh': 'Just now',
        'top_endpoints': [
            {'path': '/v1/word/{word}', 'requests': 245789, 'success_rate': 99.2, 'avg_response': 42, 'growth': 12.5},
            {'path': '/v1/synonyms/{word}', 'requests': 187456, 'success_rate': 99.5, 'avg_response': 38, 'growth': 8.7},
            # ... more endpoints
        ],
        'recent_activity': [
            {'timestamp': '2 min ago', 'endpoint': 'GET /v1/word/serendipity', 'status': 200, 'response_time': 45, 'client': '192.168.1.105'},
            # ... more activity
        ]
    }
    return render(request, 'analytics.html', context)
