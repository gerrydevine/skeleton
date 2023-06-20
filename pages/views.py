from django.shortcuts import render

def home(request):
    return render(request, "pages/home.html")

def about(request):
    return render(request, "pages/about.html")

def loggedinpage(request):
    return render(request, "pages/loggedinpage.html")
