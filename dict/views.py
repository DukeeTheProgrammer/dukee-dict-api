from django.shortcuts import render






def GetWord(request):
    pass



def DashBoard(request):
    if request.method == "GET":
        return render(request, "dashboard.html")
    else:
        pass
