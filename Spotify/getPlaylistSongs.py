import codecs
import os.path

import requests
from dotenv import dotenv_values
import util.colors as colors
import util.printWithColors as printColor

BASE_URL = "https://api.spotify.com/v1"
BASE_URL_ACCESS_TOKEN = "https://accounts.spotify.com/api/token"


def main():
    printColor.blue("Starting...")
    config = dotenv_values(".env")
    token = get_token(config)
    if token != 0:
        response = make_request_to_spotify(f'/playlists/{config["PLAYLIST_ID"]}', token)
        if response != "":
            prettify_tracks(response)
    else:
        printColor.red("Could not get token")


def init_access_token(client_credentials, client_id, client_secret):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    req = requests.post(url=f'{BASE_URL_ACCESS_TOKEN}?'
                            f'grant_type={client_credentials}&client_id={client_id}&client_secret={client_secret}',
                        headers=headers)
    response = req.json()
    if req.status_code == 200:
        file = open("access_token.txt", "w")
        file.write(response["access_token"])
        file.close()
        return response["access_token"]
    else:
        printColor.red(f'Something went wrong: {req.status_code} {response}')
        return 0


def get_token(config):
    if os.path.isfile("access_token.txt"):
        file = open("access_token.txt", "r")
        return file.read()
    else:
        printColor.blue("Getting a fresh token")
        return init_access_token("client_credentials", config["CLIENT_ID"], config["CLIENT_SECRET"])


def make_request_to_spotify(url_suffix, token):
    headers = {
        "Authorization": f'Bearer {token}'
    }

    req = requests.get(url=f'{BASE_URL}{url_suffix}?market=NO', headers=headers)
    response = req.json()
    if req.status_code == 200:
        printColor.green("Success!")
    else:
        printColor.red(f'Error getting body {req.status_code}: {response}')
        return ""

    return response


def prettify_tracks(json_response):
    tracks = json_response["tracks"]
    if tracks["total"] == tracks["limit"]:
        printColor.red("Response may have been limited!")

    playlist_name = json_response["name"]
    owner = json_response["owner"]["display_name"]

    items = tracks["items"]
    if not os.path.exists("./playlists"):
        os.mkdir("./playlists")
    playlist_file = codecs.open(f'playlists/{playlist_name}_{owner}.txt', "w", "utf-8")
    print()
    for track in items:
        track_object = track["track"]
        track_name = track_object["name"]
        artists = track_object["artists"]
        artist_names = []
        for artist in artists:
            artist_names.append(artist["name"])

        separator = ", "
        all_artists = separator.join(artist_names)

        print(f'{colors.GREEN}{track_name} {colors.BLUE}{all_artists}{colors.ENDC}')
        playlist_file.write(f'{track_name} - {all_artists}\n')

    playlist_file.close()
    print(
        f'\n\nFound {colors.GREEN}{tracks["total"]}{colors.ENDC} tracks in the playlist '
        f'{colors.GREEN}{playlist_name}{colors.ENDC} made by {colors.BLUE}{owner}{colors.ENDC} on {colors.GREEN}Spotify{colors.ENDC}')
    print(f'Playlist tracks can be found in "{playlist_file.name}"')


main()
