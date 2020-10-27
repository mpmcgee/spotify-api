import requests
import datetime
from urllib.parse import urlencode
import pybase64
client_id="28d9c25fc8574ee1bae5d06102188180"
client_secret="bdd1c3a948214ea09785ab06360b44fe"

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret):
        #super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        #returns a base64 endoded string
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id == None or client_id == None:
            raise Exception("You must set client id and client secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = pybase64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_header(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }

    def get_token_data(self):
        return{
            "grant_type": "client_credentials"
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_header()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        print(r.json())
        if r.status_code not in range(200, 299):
            return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']  # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True





#client.search
client = SpotifyAPI(client_id, client_secret)

client.perform_auth()
access_token = client.access_token
headers = {
    "Authorization": f"Bearer {access_token}"
}

endpoint = "https://api.spotify.com/v1/search"
data = urlencode({"q": "Cositas Buenas", "type": "track"})

lookup_url = f"{endpoint}?{data}"

#types are album, artist, playlist, track, show, and episode

r = requests.get(lookup_url, headers=headers)
print(r.json())
print(r.status_code)