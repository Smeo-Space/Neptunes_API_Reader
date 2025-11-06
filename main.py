import sys
import random
import time

import api
from window import WindowManager
wm = WindowManager()

wm.load()
user = 0
game = 5685

json = api.get(user,game)
print(json)
json = api.get(user+1,game)
print(json)
new_stars = [(random.uniform(-1800, 1800),
                      random.uniform(-1800, 1800),
                      random.uniform(1.0, 3.0),
                      f"New {i}") for i in range(200)]
wm.update_map(new_stars)

wm.app_exec()
time.sleep(5)