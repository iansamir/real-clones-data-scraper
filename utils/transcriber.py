"""

utils/transcriber.py

Downloads the transcript of a youtube video if available,
otherwise can download the audio to output folder

"""

import subprocess
import re
import os 

from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api import YouTubeTranscriptApi

class Transcriber:
    @staticmethod
    def clean_title(title):
        sanitized_title = re.sub(r'[\\/*?:<>|]', "", title)
        words = sanitized_title.split()[:5]  # Get first 5 words
        processed_title = "_".join(words)
        return processed_title
    

    @staticmethod
    def get_video_id(url):
        # Extract video ID from the URL
        return url.split('v=')[-1]

    @staticmethod
    def download_transcript(handle, url):
        video_id = Transcriber.get_video_id(url)
        # Attempt to get the title using yt-dlp
        try:
            result = subprocess.run(['yt-dlp', '--get-title', url], capture_output=True, text=True)
            title = result.stdout.strip()
        except Exception as e:
            print('Error fetching title:', e)
            title = video_id

        # Clean the title
        processed_title = Transcriber.clean_title(title)

        try:
            # Attempt to get the transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            # Save only the raw text to a file
            with open(f'output/transcripts/{handle}/{processed_title}.txt', 'w', encoding='utf-8') as f:
                for entry in transcript:
                    f.write(f"{entry['text']}\n")
            print(f'Transcript downloaded successfully as output/transcripts/{handle}/{processed_title}.txt')
            return processed_title
        except Exception as e:
            print(f"Unexpected error fetching transcript: {e}")
            return None

    @staticmethod
    def download_video(url):
        video_id = Transcriber.get_video_id(url)
        # Attempt to get the title using yt-dlp
        try:
            result = subprocess.run(['yt-dlp', '--get-title', url], capture_output=True, text=True)
            title = result.stdout.strip()
        except Exception as e:
            print('Error fetching title:', e)
            title = video_id

        # Clean the title
        processed_title = Transcriber.clean_title(title)

        # Attempt to download the audio using yt-dlp
        try:
            subprocess.run([
                'yt-dlp', '-x', '--audio-format', 'mp3',
                '-o', f'output/audio/{processed_title}.%(ext)s', url
            ])
            print(f'Audio downloaded successfully as output/audio/{processed_title}.mp3')
        except Exception as e:
            print('Error downloading stream:', e)
            return None

        return processed_title
    
    @staticmethod
    def download_content(handle, url):
        # Create output directories if they don't exist
        os.makedirs('output/audio', exist_ok=True)
        os.makedirs(f'output/transcripts/{handle}', exist_ok=True)

        # Try to download the transcript first
        transcript_title = Transcriber.download_transcript(handle, url)
        if transcript_title is None:
            # If transcript doesn't exist, download the audio
            # Transcriber.download_video(url) 
            return None  
        return transcript_title
    

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=D39eYe-X3gw"
    Transcriber.download_content(video_url)
