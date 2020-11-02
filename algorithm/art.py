import requests
import json

client_id = 'dd44dad17559572832be'
client_secret = 'c654b83b00eb7537b4f37d06ef9b8a31'

r = requests.post("https://api.artsy.net/api/tokens/xapp_token",
                  data={
                      "client_id": client_id,
                      "client_secret": client_secret
                  })
j = json.loads(r.text)
token = j["token"]

# создаем заголовок, содержащий наш токен
headers = {"X-Xapp-Token" : token}
# инициируем запрос с заголовком
arts = {}
with open('art.txt') as f:
    for name in f:
        r = requests.get(f"https://api.artsy.net/api/artists/{name.rstrip()}", headers=headers)
        #r.encoding = 'utf-8'
        j = json.loads(r.text)
        #print(j)
        arts[j['sortable_name']] = j['birthday']
new = sorted(arts, key=lambda x: (arts[x], x))

with open('art_new.txt', 'w') as f:
    f.writelines('\n'.join(new))