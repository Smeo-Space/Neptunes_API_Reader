import sys
import random
import time
import json
import api
from models import Star
from window import WindowManager


wm = WindowManager()

user = 2
game = 5685

json = api.get(user,game)

for _, star_data in json['stars'].items():
    if star_data is None:
        continue

    Star(star_data)

wm.load()
wm.update_map(json["stars"])
wm.app_exec()