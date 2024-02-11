import requests


from client_secrets import client_id, client_secret

AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    "scope": "user-modify-playback-state",
    'client_id': client_id,
    'client_secret': client_secret,
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

data = {"volume_percent": 10}
response = requests.put("https://api.spotify.com/v1/me/player/volume",data=data, headers=headers)
response.raise_for_status()
  

                    
