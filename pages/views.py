from django.shortcuts import render

def home(request):
    # return HttpResponse("Welcome to the Instrument ID Management System (IIMS)")
    return render(request, "pages/home.html")
