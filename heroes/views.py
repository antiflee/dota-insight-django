from django.shortcuts import render

from .models import Hero

# Create your views here.
def heroes(request):

    heroes = Hero.objects.all()

    return render(request, 'heroes/heroesHome.html', {'heroes':heroes})
