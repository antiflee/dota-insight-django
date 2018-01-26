from django.shortcuts import render
from django.http import JsonResponse

from .models import Cluster

# Create your views here.
def players(request):
    return render(request, 'players/playersHome.html')

import os
import json
from collections import defaultdict

import redis
from cassandra.cluster import Cluster as Clstr

CASSANDRA_URL = "ec2-34-213-32-67.us-west-2.compute.amazonaws.com"
cluster = Clstr([CASSANDRA_URL])
cassSession = cluster.connect("ks")

# Get num of players in each region from Redis
def realTimeRegion(request):
    date = request.GET['date']
    year, month, day = int(date[:4]), int(date[4:6]), int(date[6:])

    rows = cassSession.execute('SELECT * FROM region_num_of_players ' +
                'WHERE year=%s AND month=%s AND day=%s',
                (year, month, day))

    clusters = Cluster.objects.all()

    res = defaultdict(int)

    for row in rows:
        cluster_id, num = row.cluster_id, row.num_of_players
        cluster = Cluster.objects.filter(cluster_id=cluster_id).first()

        if not cluster:
            continue

        countries = cluster.countries.split(", ")
        for country in countries:
            res[country] += int(num)

    resJson = json.dumps(res)

    return JsonResponse(resJson,safe=False)




# Initialize clusters info
# t = """
# 111,United States,"BM, CA, PM, US"
# 112,United States,"BM, CA, PM, US"
# 114,United States,"BM, CA, PM, US"
# 121,United States,"BM, CA, PM, US"
# 122,United States,"BM, CA, PM, US"
# 123,United States,"BM, CA, PM, US"
# 124,United States,"BM, CA, PM, US"
# 131,Europe West,"GG, JE, AX, EE, FI, FO, GB, DK, IE, IM, IS, LT, LV, NO, SE, SJ, AT, BE, CH, DE, DD, FR, FX, LI, LU, MC, NL"
# 132,Europe West,"GG, JE, AX, EE, FI, FO, GB, DK, IE, IM, IS, LT, LV, NO, SE, SJ, AT, BE, CH, DE, DD, FR, FX, LI, LU, MC, NL"
# 133,Europe West,"GG, JE, AX, EE, FI, FO, GB, DK, IE, IM, IS, LT, LV, NO, SE, SJ, AT, BE, CH, DE, DD, FR, FX, LI, LU, MC, NL"
# 134,Europe West,"GG, JE, AX, EE, FI, FO, GB, DK, IE, IM, IS, LT, LV, NO, SE, SJ, AT, BE, CH, DE, DD, FR, FX, LI, LU, MC, NL"
# 135,Europe West,"GG, JE, AX, EE, FI, FO, GB, DK, IE, IM, IS, LT, LV, NO, SE, SJ, AT, BE, CH, DE, DD, FR, FX, LI, LU, MC, NL"
# 136,Europe West,"GG, JE, AX, EE, FI, FO, GB, DK, IE, IM, IS, LT, LV, NO, SE, SJ, AT, BE, CH, DE, DD, FR, FX, LI, LU, MC, NL"
# 142,South Korea,"CN, HK, JP, KP, KR, MN, MO, TW"
# 143,South Korea,"CN, HK, JP, KP, KR, MN, MO, TW"
# 151,Southeast Asia,"AF, BD, BT, IN, IR, LK, MV, NP, PK, BN, ID, KH, LA, MM, BU, MY, PH, SG, TH, TL, TP, VN"
# 152,Southeast Asia,"AF, BD, BT, IN, IR, LK, MV, NP, PK, BN, ID, KH, LA, MM, BU, MY, PH, SG, TH, TL, TP, VN"
# 153,Southeast Asia,"AF, BD, BT, IN, IR, LK, MV, NP, PK, BN, ID, KH, LA, MM, BU, MY, PH, SG, TH, TL, TP, VN"
# 161,China,"CN, HK, JP, KP, KR, MN, MO, TW"
# 163,China,"CN, HK, JP, KP, KR, MN, MO, TW"
# 171,Australia,"AU, NF, NZ"
# 181,Russia,"BG, BY, CZ, HU, MD, PL, RO, RU, SU, SK, UA"
# 182,Russia,"BG, BY, CZ, HU, MD, PL, RO, RU, SU, SK, UA"
# 183,Russia,"BG, BY, CZ, HU, MD, PL, RO, RU, SU, SK, UA"
# 184,Russia,"BG, BY, CZ, HU, MD, PL, RO, RU, SU, SK, UA"
# 191,Europe East,"BG, BY, CZ, HU, MD, PL, RO, RU, SU, SK, UA"
# 200,South America,"AR, BO, BR, CL, CO, EC, FK, GF, GY, PE, PY, SR, UY, VE"
# 204,South America,"AR, BO, BR, CL, CO, EC, FK, GF, GY, PE, PY, SR, UY, VE"
# 211,South Africa,"BW, LS, NA, SZ, ZA"
# 212,South Africa,"BW, LS, NA, SZ, ZA"
# 213,South Africa,"BW, LS, NA, SZ, ZA"
# 221,China,"CN, HK, JP, KP, KR, MN, MO, TW"
# 222,China,"CN, HK, JP, KP, KR, MN, MO, TW"
# 223,China,"CN, HK, JP, KP, KR, MN, MO, TW"
# 231,China,"CN, HK, JP, KP, KR, MN, MO, TW"
# """
#
# for id_, name, countries in [x.split(",",2) for x in t.split("\n")[1:-1]]:
#     obj, created = Cluster.objects.get_or_create(
#         cluster_id=int(id_)
#     )
#     obj.region=name
#     obj.countries=countries.strip('"')
#     obj.save()
