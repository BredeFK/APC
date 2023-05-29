using Microsoft.AspNetCore.Mvc;
using SoulseekAPI.Models;
using SoulseekAPI.Service;

namespace SoulseekAPI.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class SoulseekSongsController : ControllerBase
    {
        private readonly SoulSeekService _soulSeekService;
        private readonly ILogger<SoulseekSongsController> _logger;

        public SoulseekSongsController(
            ILogger<SoulseekSongsController> logger,
            SoulSeekService soulSeekService

            )
        {
            _logger = logger;
            _soulSeekService = soulSeekService;
        }

        [HttpGet(Name = "GetSoulseekSongs")]
        public async Task<List<Track>> Get(string song, string artist, string? filterType, string exclude, long? minSize, long? maxSize)
        {
            _logger.LogInformation("GET " + song + " by " + artist);
            var list = await _soulSeekService.GetTracks(song, artist, filterType, exclude, minSize, maxSize);
            return list;
        }

        [HttpPost(Name = "DownloadSoulseekSong")]
        public async Task Post(Track track, string folder)
        {
            _logger.LogInformation("POST " + track.Name + " to folder " + folder);
            await _soulSeekService.DownloadTrack(track, folder);
        }
    }
}