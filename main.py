import sys
import random

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