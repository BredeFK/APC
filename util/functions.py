from datetime import datetime
import util.colors as colors
import util.printWithColors as printColor


def get_date_and_time():
    return datetime.now().strftime("%d%m%Y_%H.%M.%S")


def finished_print(diff):
    printColor.blue(f'Finished! Total time: {round(diff, 2)} s. ({round(diff / 60, 2)} min.)')


def print_spotify_details(total_tracks, playlist_name, owner, playlist_txt_file, playlist_json_file):
    print(
        f'\n\nFound {colors.GREEN}{total_tracks}{colors.ENDC} tracks in the playlist '
        f'{colors.GREEN}{playlist_name}{colors.ENDC} made by '
        f'{colors.BLUE}{owner}{colors.ENDC} on {colors.GREEN}Spotify{colors.ENDC}\n'
        f'Playlist tracks in text format can be found in {colors.BLUE}{playlist_txt_file}{colors.ENDC}\n'
        f'Playlist tracks in JSON format can be found in {colors.BLUE}{playlist_json_file}{colors.ENDC}\n'
    )
