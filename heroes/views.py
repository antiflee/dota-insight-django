from django.shortcuts import render
from django.http import JsonResponse

from .models import Hero

# Open sessions to Redis and Cassandra

import redis
import os
import json

HOSTURL = "ec2-34-213-4-249.us-west-2.compute.amazonaws.com"
r = redis.StrictRedis(host=HOSTURL, port=6379, db=0)

from cassandra.cluster import Cluster

CASSANDRA_URL = "ec2-34-213-32-67.us-west-2.compute.amazonaws.com"
cluster = Cluster([CASSANDRA_URL])
cassSession = cluster.connect("ks")

# Create your views here.
def heroes(request):

    heroes = Hero.objects.all()

    return render(request, 'heroes/heroesHome.html', {'heroes':heroes})

def heroDetail(request, pk):
    heroes = Hero.objects.all()
    # Retrieve basic info of the hero from local DB sqlite3
    theHero = Hero.objects.filter(hero_id=pk).first()
    # To-do: Retriev real time info of the hero from database (Cassandra?)
    #

    if not theHero:
        return render(request, 'heroes/heroesHome.html',{'heroes':heroes})

    heroPairs = getHeroPairsWinRate(pk)

    for i in range(len(heroPairs)):
        winRate, heroId = heroPairs[i]
        winRate = str(int(float(winRate)*100))+"%"
        hero = Hero.objects.filter(hero_id=heroId).first()
        heroPairs[i] = (heroId, hero.imageUrl, winRate)

    return render(request,
                'heroes/heroDetail.html',
                {'theHero':theHero, 'heroes':heroes, 'heroPairs':heroPairs})

# Get the win rate for all heroes. Return a json file.

def getHeroesWinRate(request):

    # HOSTURL = os.environ.get('AWS_REDIS_URL')
    # print(HOSTURL)

    res = {}

    for heroId in range(1, 120):
        winRate = r.get(heroId)
        if winRate:
            res[heroId] = winRate.decode("utf-8")

    resJson = json.dumps(res)

    return JsonResponse(resJson,safe=False)

# Get the win rate of a specific hero pairing with all other heroes
# (Not used) Returns a dictionary: key: another hero's id, value: win rate.
# Returns a list of max 10 heroes that ordered by win rate (high to low).

def getHeroPairsWinRate(heroId):

    res = []

    for i in range(1, 120):
        if i != heroId:
            key = str(heroId)+","+str(i)
            winRate = r.get(key)

            if winRate is not None:
                res.append((winRate.decode("utf-8"),i))

    res.sort(key=lambda x: x[0], reverse=True)
    res = res[:min(len(res), 10)]

    return res


# Get the win rate of a specific hero pairing with all other heroes
# (Not used) Returns a dictionary: key: another hero's id, value: win rate.
# Returns a list of max 10 heroes that ordered by win rate (high to low).

def getHeroPairsWinRate(heroId):

    res = []

    for i in range(1, 120):
        if i != heroId:
            key = str(heroId)+","+str(i)
            winRate = r.get(key)

            if winRate is not None:
                res.append((winRate.decode("utf-8"),i))

    res.sort(key=lambda x: x[0], reverse=True)
    res = res[:min(len(res), 10)]

    return res


# Query Cassandra for the historical win rate of a hero

def getHeroWinRateHistory(request, pk):

    heroId = pk
    rows = cassSession.execute('SELECT * FROM hero_win_rate WHERE hero_id=%s', (str(heroId),))
    dates, win_rates, counts = [], [], []

    for row in rows:
        dates.append(formatDate(row.year,row.month,row.day))
        win_rates.append(round(row.win_rate,3))
        counts.append(row.count)

    res = {'dates':dates,'win_rates':win_rates,'counts':counts}

    resJson = json.dumps(res)

    return JsonResponse(resJson,safe=False)

def formatDate(year,month,day):
    # From integers to yyyy-MM-dd
    return str(year) + "-" + str(month) + "-" + str(day)
