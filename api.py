import requests


user = 1
game = 5685
with open("keys.txt") as fkey:
    for i, line in enumerate(fkey):
        if i == user:
            key = line.rstrip()

ip = f"https://np.ironhelmet.com/api?game_number={game}&code={key}"

x = requests.get(ip)
f = open(f"api_user_{user}.json","w")

f.write(x.text)
f.close()