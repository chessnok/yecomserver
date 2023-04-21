import time

from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from datetime import datetime
import os
import clickhouse_connect

from django.shortcuts import render


def serve_site_files(request, path):
    file_path = os.path.join(settings.BASE_DIR, 'site', path)
    if os.path.exists(file_path):
        return render(request, file_path)
    else:
        return HttpResponse("File not found")


class DataAggregator:
    def __init__(self, userid="user_10000", sessionid=593, timestamp='2025-01-04T12:00', action="mainpage",
                 value=0, category=None, age=18, gender="М", city="Москва", from_=None):
        self.userid = userid
        self.sessionid = sessionid
        self.timestamp = timestamp
        self.action = action
        self.value = value
        self.category = category
        self.age = age
        self.gender = gender
        self.city = city
        self.from_ = from_

    def get_string(self):
        return f"{self.userid},{self.sessionid},{self.from_},{self.timestamp},{self.action},{self.value},{self.category},{self.age},{self.gender},{self.city}"


def new_action(request):
    # аргументы - request.POST.get('')
    data = DataAggregator(
        userid=request.POST.get('userid', 'user_10000'),
        sessionid=request.POST.get('sessionid', 593),
        timestamp=request.POST.get('timestamp', '2025-01-04T12:00'),
        action=request.POST.get('action', 'mainpage'),
        value=request.POST.get('value', 0),
        category=request.POST.get('category', ""),
        age=request.POST.get('age', 18),
        gender=request.POST.get('gender', "М"),
        city=request.POST.get('city', 'Москва'),
        from_=request.POST.get('from_', "")
    )
    if "log.csv" not in os.listdir("./data"):
        with open("./data/log.csv", "ab") as f:
            f.write("userid,sessionid,from,timestamp,action,value,category,age,gender,city\n".encode("UTF-8"))
    with open("./data/log.csv", "ab") as f:
        f.write((data.get_string() + '\n').encode("UTF-8"))
    return HttpResponseRedirect("/site/index.html?send=1")
