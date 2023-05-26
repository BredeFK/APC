# Folder: Spotify

## What you need

* Python 3.10
* A developer user for
  Spotify, [see tutorial](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)
* An .env file that looks like below:
    * `PLAYLIST_ID` will probably be solved another way later

```.env
CLIENT_ID="<clientid>"
CLIENT_SECRET="<clientsecret>"
PLAYLIST_ID="<playlistid>"
```

<small>Last updated 2023-05-26</small>

## How to get the playlistID

1. Go to spotify and select the playlist you want to use
2. Right-click on the playlist, select `Share` and `Copy link to playlist`
3. The URL will look something like this https://open.spotify.com/playlist/5ABMzUESx7K7EyowE5kFCl?si=067d7a2f9a4246a1
4. The playlistID is the part after `playlist/`, in this URL, it's `5ABMzUESx7K7EyowE5kFCl`

## Run the stuff

Do and have the above and then run the script, and you should get a nice message.
The playlist songs will end up in the folder `/playlists/<playlist_name>_<playlist_creator>.txt`