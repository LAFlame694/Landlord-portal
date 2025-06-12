import requests
from requests.auth import HTTPBasicAuth

consumer_key = "idleymLNb9P0iWtRaumKDVDxjjt205CTGLwSMwtDkJ65ZSR8"
consumer_secret = "UoCdbcwlFFGUNtRqt9iA2AP5R9mnjqTrKanwDMTvhrKM42UohTkAREFGIUPmqm6q"

api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

response = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

print(response.status_code)
print(response.json())