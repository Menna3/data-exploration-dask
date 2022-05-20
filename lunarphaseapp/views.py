import datetime
import decimal
import math

from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response


def position(now=None):
    if not now:
        now = datetime.datetime.now()

    dec = decimal.Decimal
    diff = now - datetime.datetime(2001, 1, 1)
    days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
    lunations = dec("0.20439731") + (days * dec("0.03386319269"))
    return lunations % dec(1)


def phase(position):
    dec = decimal.Decimal
    index = (position * dec(8)) + dec("0.5")
    index = math.floor(index)
    return {
        0: "New Moon",
        1: "Waxing Crescent",
        2: "First Quarter",
        3: "Waxing Gibbous",
        4: "Full Moon",
        5: "Waning Gibbous",
        6: "Last Quarter",
        7: "Waning Crescent"
    }[int(index) & 7]


class LunarphaseAPIView(APIView):
    def get(self, request):
        pos = position()
        phase_name = phase(pos)
        rounded_position = round(float(pos), 3)

        response = {
            "phase_name": phase_name,
            "rounded_position": rounded_position
        }

        return Response(response)


class IndexView(View):

    def get(self, request):
        pos = position()
        phase_name = phase(pos)
        rounded_position = round(float(pos), 3)

        context = {
            "phase_name": phase_name,
            "rounded_position": rounded_position
        }

        return render(request, "home.html", context)


