from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def home(request):
    return render(request, "pages/home.html")

def about(request):
    return render(request, "pages/about.html")

@login_required
def loggedinpage(request):
    return render(request, "pages/loggedinpage.html")
