from django.shortcuts import render
from django.http import JsonResponse

from .models import Hero

# Create your views here.
def heroes(request):

    heroes = Hero.objects.all()

    return render(request, 'heroes/heroesHome.html', {'heroes':heroes})



# Get the win rate for all heroes. Return a json file.

import redis
import os
import json

def getHeroesWinRate(request):

    # HOSTURL = os.environ.get('AWS_REDIS_URL')
    # print(HOSTURL)
    HOSTURL = "ec2-34-213-4-249.us-west-2.compute.amazonaws.com"
    r = redis.StrictRedis(host=HOSTURL, port=6379, db=0)

    res = {}

    for heroId in range(1, 120):
        winRate = r.get(heroId)
        if winRate:
            res[heroId] = winRate.decode("utf-8")

    resJson = json.dumps(res)

    return JsonResponse(resJson,safe=False)
