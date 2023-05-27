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

        public async Task<List<Track>> GetTracks(string songName, string? filterType, int? minSize, int? maxSize)
        {
            await Connect();
            var query = SearchQuery.FromText(songName);
            var searchResults = await _soulseekClient.SearchAsync(query);
            var tracks = GetTrackList(searchResults.Responses);

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

            list = list.OrderByDescending(x => x.Size).Take(10).ToList();


            return list;
        }

        public async Task DownloadTrack(Track track)
        {
            await Connect();
            await _soulseekClient.DownloadAsync(track.Username, track.OriginalName, track.Name);

        }

        private List<Track> GetTrackList(IReadOnlyCollection<SearchResponse> response)
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
                        Size = file.Size
                    };

                    list.Add(track);
                }
            }
            return list;
        }
    }
}
