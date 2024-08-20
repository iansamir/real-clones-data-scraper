"""

Real Clones Data Scraper

Scrapes YouTube transcripts from any channel and 
uploads them as OpenAI embedding vectors to Pinecone DB.

"""

import argparse 
from utils.process_text import TextProcessor
from utils.fetch_videos import ChannelScraper
from utils.transcriber import Transcriber
import os

def parse_args(): 
    # parse arguments and return a dictionary
    parser = argparse.ArgumentParser(description="Real Clones Data Scraping Tool")
    parser.add_argument(
        "channel_handle", 
        type=str, 
        nargs='?',
        default="@ArlinMoore", 
        help="YouTube Channel Handle. Default value is @ArlinMoore."
    )
    parser.add_argument(
        "num_videos", 
        type=int, 
        nargs='?', 
        default=20, 
        help="Number of latest videos to fetch. Default value is 20"
    )
    
    args = parser.parse_args() 

    return args 

def main():
    # Get arguments from parser 
    args = parse_args() 

    # Ensure the existence of output folders
    output_folder = os.path.join("output", args.channel_handle, "transcripts")
    os.makedirs(output_folder, exist_ok=True)

    # Download the transcripts of all the videos 
    video_urls = ChannelScraper.get_latest_video_urls(args.channel_handle, args.num_videos)
    print(*video_urls, sep="\n") 
    for url in video_urls:
        Transcriber.download_content(args.channel_handle, url)

if __name__ == "__main__":
    main()
