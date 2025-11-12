import sys
import random
import time
import json
import api
from models import Star, Player, Fleet
from window import WindowManager


wm = WindowManager()

user = 2
game = 5685

json = api.get(user,game)

# Loading data into classes
#TODO: Put these somewhere better
for _, player_data in json['players'].items():
    if player_data is None:
        continue

    Player(player_data)

for _, star_data in json['stars'].items():
    if star_data is None:
        continue

    Star(star_data)

for _, fleet_data in json['fleets'].items():
    if fleet_data is None:
        continue

    Fleet(fleet_data)

wm.load()
wm.update_map(Star.get_all())
wm.app_exec()
