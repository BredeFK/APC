import time
import requests
from requests import ConnectTimeout

import util.printWithColors as printColor
import util.colors as colors

BASE_URL_API = "https://localhost:7069"
TIMEOUT_IN_SECONDS = (5 * 60)  # 5 Minutes


def search_for_song(index, artist, song, filter_type, exclude, min_size, max_size):
    printColor.blue(f'{index}: Searching for {song} by {artist}...')
    headers = {
        "Accept": 'Application/json'
    }

    try:
        start = time.time()
        req = requests.get(
            url=f'{BASE_URL_API}/SoulseekSongs'
                f'?song={song}&artist={artist}&filterType={filter_type}&exclude={exclude}&minSize={min_size}',
            headers=headers,
            verify=False,
            timeout=TIMEOUT_IN_SECONDS
        )
        end = time.time()
        if req.status_code == 200:
            response = req.json()
            if len(response) != 0:
                printColor.green(f'Success: Found {len(response)} songs in {round(end - start, 2)} seconds')
                return response[0]
            else:
                printColor.red(f'Could not find {song} by {artist}')
                return None
        else:
            printColor.red(f'Could not find any results for {song} by {artist}, got {req.status_code}')
            return None
    except ConnectTimeout:
        printColor.red(f'Could not find any results for {song} by {artist}, ConnectTimeout')
        return None
    except Exception:
        printColor.red("Something went wrong with searching for songs")


def download_song(song, folder_name):
    print(f'Downloading {colors.GREEN}{song["name"]}{colors.ENDC}')

    try:
        start = time.time()
        req = requests.post(
            url=f'{BASE_URL_API}/SoulseekSongs?folder={folder_name}',
            json=song,
            verify=False,
            timeout=TIMEOUT_IN_SECONDS
        )
        end = time.time()

        if req.status_code == 200:
            printColor.green(f'Success: Downloaded {song["name"]} in {round(end - start, 2)} seconds')
        else:
            printColor.red(
                f'Could not download {song["name"]} in {round(end - start, 2)} seconds, got {req.status_code}')
    except ConnectTimeout:
        printColor.red(f'Could not download song {song["name"]}, ConnectTimeout')
    except Exception:
        printColor.red(f'Something went wrong with downloading song {song["name"]}')
