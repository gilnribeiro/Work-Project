import requests
from config import CLIENT_ID, API_KEY

# url = "https://indeed-indeed.p.rapidapi.com/apigetjobs"

# querystring = {"publisher":CLIENT_ID,"jobkeys":API_KEY,"v":"2","format":"json"}

# headers = {
#     'x-rapidapi-host': "indeed-indeed.p.rapidapi.com",
#     'x-rapidapi-key': "SIGN-UP-FOR-KEY"
#     }

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)

# url = "https://apis.indeed.com/oauth/v2/tokens"

# headers = {
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'Accept': 'application/json',
#     'client_id': CLIENT_ID,
#     'client_secret': API_KEY,
# }

# params = {
#     'grant_type': 'client_credentials',
#     'scope': 'employer_acces'
# }

# response = requests.request("POST", url, headers=headers, params=params)

# url = "https://secure.indeed.com/v2/api/appinfo"

# headers = {
#     ''
# }

api_url = 'http://api.indeed.com/ads/apisearch?publisher={}v=2&limit=100000&format=json'

urlfirst = api_url + '&co=pt' + '&q='

response = requests.get(urlfirst)

