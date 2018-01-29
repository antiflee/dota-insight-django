from django.shortcuts import render,redirect

def home(request):
    print("home-----")
    return redirect("/heroes/")
    return render(request, "home.html", {})
