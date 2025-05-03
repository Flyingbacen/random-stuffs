from discord import SyncWebhook
import requests
import json
import time

file_parts = __file__.split("\\")
file_parts.pop()
filedir = "\\".join(file_parts) + "\\"
with open(filedir + "authcodes.json", "r") as f:
    authcodes = json.load(f)
    """
    example_authcodes = {
    "secret": "client secret",
    "client_id": "client id",
    "Authorization": "OAuth token",
    "webhook_url": "webhook url"
    }
    """
    if "secret" not in authcodes:
        authcodes["secret"] = input("Enter your client secret: ")
    if "client_id" not in authcodes:
        authcodes["client_id"] = input("Enter your client id: ")
    if "Authorization" not in authcodes:
        authcodes["Authorization"] = input("Enter your OAuth token: ")
    json.dump(authcodes, open(filedir + "authcodes.json", "w"))

wantedstreamers = ["pksparkxx", "auralaur67", "juiceprophet", "one_shot_gurl", "trickygym", "PokemonGO", "PokemonGOAppLA", "PokemonGOAppBR", "Pokemon", "PKMNcast", "CoupleOfGamingTV", "KeibronGamerYT", "alfindeol", "PokemonProfessorNetwork"]
wantedgames = ["Pokémon Trading Card Game", "Pokémon GO", "Pokémon Trading Card Game Live"]

webhook = SyncWebhook.from_url(authcodes["webhook_url"])

def refreshAuth():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post("https://id.twitch.tv/oauth2/token?client_id=" + authcodes["client_id"] + "&client_secret=" + authcodes["secret"] + "&grant_type=client_credentials", headers=headers)
    authcodes["Authorization"] = response.json()["access_token"]
    json.dump(authcodes, open(filedir + "authcodes.json", "w"))

def sendRequest():
    headers = {
        "Client-Id": authcodes["client_id"],
        "Authorization": "Bearer " + authcodes["Authorization"]
    }
    query_string = "&" + "&".join(f"user_login={i}" for i in wantedstreamers)
    response = requests.get("https://api.twitch.tv/helix/streams?type=live" + "&" + "&".join(f"user_login={i}" for i in wantedstreamers), headers=headers)
    # print(response.json())
    try:
        for streamdata in response.json()["data"]:
            if streamdata["game_name"] in wantedgames:
                webhook.send(f"{streamdata['user_name']} is streaming {streamdata['game_name']} with {streamdata['viewer_count']} viewers! {streamdata['title']}\nLink: https://twitch.tv/{streamdata['user_login']}")
        if response.json()["data"] == []:
            print("No streams found")
        if "message" in response.json():
            if "Invalid OAuth token" in response.json()["message"] or "Unauthorized" in response.json()["error"]:
                print("Invalid OAuth token")
                refreshAuth()
                sendRequest()
    except Exception as e:
        print(e)
        input()
    example_response = {
        'data': [
            {'id': '51857208141',
            'user_id': '88398526',
            'user_login': 'one_shot_gurl',
            'user_name': 'ONE_shot_GURL',
            'game_id': '9618',
            'game_name': 'Pokémon Trading Card Game',
            'type': 'live',
            'title': '🔴 DROPS 🔴 Opening Tons of Fun Pokemon Packs!',
            'viewer_count': 376,
            'started_at': '2024-08-25T22:12:40Z',
            'language': 'en',
            'thumbnail_url': 'https://static-cdn.jtvnw.net/previews-ttv/live_user_one_shot_gurl-{width}x{height}.jpg',
            'tag_ids': [],
            'tags': [
                'FamilyFriendly',
                'ChatReader',
                'English',
                'girlgamers',
                'pokemon',
                'openingpacks',
                'openingcards',
                'pokemoncontent',
                'pokemoncards',
                'livebreaks'
            ],
            'is_mature': False
            }
        ],
        'pagination': {
            'cursor': ''
        }
    }
    # print(link)

while True:
    sendRequest()
    print("Finished request")
    time.sleep(60*5)