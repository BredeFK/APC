using Microsoft.OpenApi.Services;
using Soulseek;
using System.Collections.Generic;
using SoulseekAPI.Controllers;
using SoulseekAPI.Models;

namespace SoulseekAPI.Service
{
    public class SoulSeekService
    {
        private readonly SoulseekClient _soulseekClient;
        private bool _isConnected;
        private readonly ILogger<SoulSeekService> _logger;


        public SoulSeekService(
            ILogger<SoulSeekService> logger,
            SoulseekClient soulseekClient
            )
        {
            _logger = logger;
            _soulseekClient = soulseekClient;
            _isConnected = false;
        }

        private async Task Connect()
        {
            if (!_isConnected)
            {
                await _soulseekClient.ConnectAsync("Username", "Password");
                _isConnected = true;
            }
        }

        public async Task<List<Track>> GetTracks(string songName, string artist, string? filterType, string exclude, long? minSize, long? maxSize)
        {
            await Connect();

            var excludeList = exclude.Split(',').ToList();
            excludeList.RemoveAt(excludeList.Count - 1);

            var query = SearchQuery.FromText(songName + " " + artist);
            var searchResults = await _soulseekClient.SearchAsync(query);
            var tracks = GetTrackList(searchResults.Responses, songName, excludeList);

            var list = tracks;

            if (filterType != null)
            {
                list = list.Where(track => track.Type == filterType).ToList();
            }

            if (minSize != null)
            {
                list = list.Where(track => track.Size >= minSize).ToList();
            }

            if (maxSize != null)
            {
                list = list.Where(track => track.Size <= maxSize).ToList();
            }

            if (list.Count == 0)
            {
                _logger.LogWarning("Couldn't find any songs with specified filters, default to all");
                list = tracks;
            }

            list = list.OrderBy(x => x.HasFreeUploadSlot).ThenByDescending(x => x.Size).ThenBy(x => x.UploadSpeed).Take(10).ToList();


            return list;
        }

        public async Task DownloadTrack(Track track, string folder)
        {
            await Connect();
            var path = "Songs\\" +folder + "\\" + track.Name;

            try
            {
                await _soulseekClient.DownloadAsync(track.Username, track.OriginalName, path);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex.ToString(), ex);
            }

        }

        private List<Track> GetTrackList(IReadOnlyCollection<SearchResponse> response, string songName, List<string> excludeList)
        {
            var list = new List<Track>();
            foreach (var result in response)
            {
                foreach (var file in result.Files)
                {
                    var track = new Track()
                    {
                        Username = result.Username,
                        Name = file.Filename.Split('\\').Last(),
                        OriginalName = file.Filename,
                        Type = file.Filename.Split('.').Last(),
                        Size = file.Size,
                        QueueLength = result.QueueLength,
                        UploadSpeed = result.UploadSpeed,
                        HasFreeUploadSlot = result.HasFreeUploadSlot
                    };

                    var trackName = track.Name.ToUpper();
                    if (trackName.Contains(songName.ToUpper()) && track.QueueLength <= 5)
                    {
                        var containsName = false;
                        foreach (var excludeName in excludeList)
                        {
                            if (trackName.Contains(excludeName.ToUpper()))
                            {
                                containsName = true;
                            }
                        }

                        if (!containsName)
                        {
                            list.Add(track);
                        }
                    }
                }
            }
            return list;
        }
    }
}
