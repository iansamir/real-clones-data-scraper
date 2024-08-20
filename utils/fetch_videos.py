"""

fetch_videos.py

Fetches list of youtube video links from a given YouTube 
channel by handle, ex. @ArlinMoore 

"""

import yt_dlp

class ChannelScraper:
    @staticmethod
    def get_channel_url(handle):
        channel_url = f'https://www.youtube.com/c/{handle}'
        return channel_url 

    @staticmethod
    def get_latest_video_urls(handle, num_videos=5):
        channel_url = ChannelScraper.get_channel_url(handle)
        print(f"Scraping {handle} channel ...")
        # Set up yt-dlp options
        ydl_opts = {
            'quiet': True,  # Suppress output
            'extract_flat': True,  # Extract only video URLs
        }

        # Create a YouTubeDL instance with the options
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract the playlist (channel's videos)
            result = ydl.extract_info(channel_url, download=False)
            # Extract URLs safely
            video_urls = [entry.get('url', 'No URL') for obj in result.get('entries', []) for entry in obj.get('entries', [])]
        
        print("Video Links: ")
        print(*video_urls[:num_videos], sep="\n")
        return video_urls[:num_videos]

        
if __name__ == "__main__":
    handle = "@ArlinMoore"
    num_videos = 50
    latest_video_urls = ChannelScraper.get_latest_video_urls(handle, num_videos)

    # Print the URLs
    for url in latest_video_urls:
        print(url)
