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
        public async Task<List<Track>> Get(string songName, string? filterType, int? minSize, int? maxSize)
        {
            var list = await _soulSeekService.GetTracks(songName, filterType, minSize, maxSize);

            return list;
        }

        [HttpPost(Name = "DownloadSoulseekSong")]
        public async Task Post(Track track)
        {
            await _soulSeekService.DownloadTrack(track);

        }
    }
}