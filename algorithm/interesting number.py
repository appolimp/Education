import requests

proxies = {
  'https': 'http://82.119.170.106:8080',
}

res = requests.get('https://numbersapi.com', proxies=proxies)

print(res.status_code)