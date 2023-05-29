namespace SoulseekAPI.Models
{
    public class Track
    {
        public string Name { get; set; }
        public string Username { get; set; }
        public string OriginalName { get; set; }
        public string Type { get; set; }
        public long Size { get; set; }
        public long UploadSpeed { get; set; }
        public int QueueLength { get; set; }
        public bool HasFreeUploadSlot { get; set; }
    }
}
