import codecs
import json
import os.path
import time
import requests
import urllib3
import util.colors as colors
import util.printWithColors as printColor
import util.functions as functions
import soulseekService

from dotenv import dotenv_values

BASE_URL = "https://api.spotify.com/v1"
BASE_URL_ACCESS_TOKEN = "https://accounts.spotify.com/api/token"


def main():
    urllib3.disable_warnings()
    ans = input("Do you want to use songs from .json file (y/n)?:")
    if ans.upper() == 'Y':
        file_name = input("Enter complete file name:")
        read_tracks_from_file(file_name)
    else:
        start = time.time()
        config = dotenv_values(".env")
        token = get_token(config)
        if token != 0:
            response = make_request_to_spotify(f'/playlists/{config["PLAYLIST_ID"]}', token)
            if response != "":
                process_tracks(response)
                end = time.time()
                functions.finished_print(end - start)
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
        print(
            f'Found playlist on Spotify called {colors.GREEN}{response["name"]}{colors.ENDC} '
            f'containing {colors.GREEN}{len(response["tracks"]["items"])}{colors.ENDC} songs')
    else:
        printColor.red(f'Error getting body {req.status_code}: {response}')
        return ""

    return response


def process_tracks(json_response):
    tracks = json_response["tracks"]
    if tracks["total"] == tracks["limit"]:
        printColor.red("Response may have been limited!")

    playlist_name = json_response["name"]
    owner = json_response["owner"]["display_name"]

    items = tracks["items"]
    if not os.path.exists("./playlists"):
        os.mkdir("./playlists")

    playlist_name_prefix = f'{playlist_name}_{functions.get_date_and_time()}'
    playlist_file = codecs.open(f'playlists/{playlist_name_prefix}.txt', "w", "utf-8")
    print()
    soulseek_songs = []
    no_result_songs = []
    for index, track in enumerate(items):
        track_object = track["track"]
        track_name = track_object["name"]
        artists = track_object["artists"]
        artist_names = []
        for artist in artists:
            artist_names.append(artist["name"])

        separator = ", "
        all_artists = separator.join(artist_names)

        playlist_file.write(f'{track_name} - {all_artists}\n')
        song = soulseekService.search_for_song((index + 1), all_artists, track_name, "flac", "edit,", 100000, 0)
        if song is not None:
            soulseek_songs.append(song)
        else:
            no_result_songs.append(f'{track_name} by {all_artists}')

    playlist_file.close()

    playlist_json = codecs.open(f'playlists/{playlist_name_prefix}.json', "a", "utf-8")
    json.dump(soulseek_songs, playlist_json)
    playlist_json.close()

    functions.print_spotify_details(tracks["total"], playlist_name, owner, playlist_file.name, playlist_json.name)

    if len(soulseek_songs) > 0:
        printColor.green(
            f'Found {len(soulseek_songs)} of {tracks["total"]} songs on Soulseek, starting download now...')
        download_songs(soulseek_songs, playlist_name)
    else:
        printColor.red(f'Could not find any songs on Soulseek :(')
        for song in no_result_songs:
            printColor.red(f'Could not find {song}')


def read_tracks_from_file(file_name):
    path = f'./playlists/{file_name}'
    if os.path.exists(path) and file_name.endswith(".json"):
        printColor.green(f'Parsing file "{file_name}" now...')
        file = open(path, 'r')
        songs = json.load(file)
        playlist_name = file_name.split("_")[0]
        start = time.time()
        download_songs(songs, playlist_name)
        functions.finished_print(time.time() - start)
    else:
        printColor.red(f'Could not find a file named "{file_name}"')


def download_songs(songs, playlist_name):
    folder_name = f'{playlist_name}_{functions.get_date_and_time()}'
    if not os.path.exists(f'../SoulseekAPI/SoulseekAPI/Songs{folder_name}'):
        os.mkdir(f'../SoulseekAPI/SoulseekAPI/Songs/{folder_name}')
    for song in songs:
        soulseekService.download_song(song, folder_name)


main()
