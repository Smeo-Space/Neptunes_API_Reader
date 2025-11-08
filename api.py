import requests
import json

_json = {}
def get(user,game):
	with open("keys.txt") as fkey:
		for i, line in enumerate(fkey):
			if i == user:
				key = line.rstrip()

	ip = f"https://np.ironhelmet.com/api?game_number={game}&code={key}"

	data = requests.get(ip)
	json = data.json()["scanning_data"]
	global _json
	_json = json
	return json

def json():
	return _json