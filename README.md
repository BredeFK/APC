# APC : Automated Playlist Converter

## About

This is a repository for trying to automatically convert Spotify (and potentially other services') playlists.

### SoulseekAPI

Not really a script, and more like a .NET project. This is needed as I couldn't find an API for Soulseek, but found a
.NET package. I will probably try to have this on Azure functions some time. It currently has two endpoints, one for
getting search results and one for downloading songs.

### Spotify

Spotify-folder is (currently) for writing all tracks from a specified playlist
in to a file. There will be another README file in each category explaining further how it works.

### Organize_Folder

This folder is to get all song files in one folder, so you don't have to go in to each folder in a folder in a folder to
move them out. This will not delete the empty folders afterwards, only move the songs.

#### Example

File structure before: <br>

```
complete/userxD/another_folder/KJØPE HELE SVERIGE.flacc
complete/tempyBoi/01.02.2023 - DNB /hackers.mp3
complete/tempyBoi/12.12.2020 - Pop /baby.mp3
```

File structure after: <br>

```
songs/KJØPE HELE SVERIGE.flacc
songs/hackers.mp3
songs/baby.mp3
```

## Other

* The scripts are written using IntelliJ
* The scripts are running on Python version 3.10

## Documentation for stuff

### Spotify

https://developer.spotify.com/documentation/web-api/tutorials/getting-started