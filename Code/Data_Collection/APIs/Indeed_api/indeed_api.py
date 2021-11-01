import requests
from config import CLIENT_ID, API_KEY


class IndeedApi():
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'client_id': CLIENT_ID,
            'client_secret': API_KEY,
        }
        self.session.params = {
            'grant_type': 'client_credentials', 
            'scope': 'employer_access'
        }

    def get_authorization_code(self):
        self.session.params = {
            'client_id': CLIENT_ID,
            'redirect_uri': "https%3A%2F%2Fgilnribeiro.github.io%2F",
            'response_type': 'code',
            'state': 'employer1234',
            'scope': 'email+offline_access+employer_access'

        }

        return self.session.get('https://secure.indeed.com/oauth/v2/authorize').json()

    def get_access_token(self, code):
        self.session.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
        }
        self.session.params = {
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': API_KEY,
            'redirect_uri': "https%3A%2F%2Fgilnribeiro.github.io%2F",
            'grant_type': 'authorization_code', 
        }
        return self.session.post('https://apis.indeed.com/oauth/v2/tokens').json()

    

Indeed = IndeedApi()
authorization_code = Indeed.get_authorization_code()
acess_token = Indeed.get_access_token(authorization_code['code'])
Indeed.get_jobs()
