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

## Run the stuff

For now you need to do the above and run the script once. If everything went good, you will get this message:

```
Starting...
Getting a fresh token
Error getting body 401: {'error': {'status': 401, 'message': 'Invalid access token'}}
```

Then you run it again, and you should get a better message. This *could* be solved in a nicer way, but im lazy