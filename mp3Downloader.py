#!/usr/bin/env python3
import yt_dlp
import os
import sys
import argparse

# Playlist link passed in
PLAYLIST = sys.argv[1]
#PLAYLIST = "https://www.youtube.com/playlist?list=PLDWJwqI-7Ru-7pjP3k6zKkPbuAYzJ0ZyT"

# Video download function
def downloadVideo(inlink):
    ydl_opts = {    # Options for download
        'format': 'bestaudio/best',
        'ignoreerrors': True,           # Ingores odd errors that are produced by the library
        'no_warnings': True,
        'ignoreerrors': True,
        'download_archive': 'archive.txt',
        'quiet': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',# codec used
            'preferredcodec': 'mp3',    # Extracts in mp3
            'preferredquality': '192'
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(inlink)

# Argument parser for the values that we will pass in to the program
parser = argparse.ArgumentParser(description='Process Downloader options')
parser.add_argument('--path',
                    help='Save location for songs Ex. --path ')
parser.add_argument('--playlist',
                    help='Link to the playlist that will be downloaded')
args = parser.parse_args()
#reference argument with args.playlist
#reference argument with args.path


try:
    # Makes new directory according to the input supplied by command line arguments
    playlist_dir_name = args.path
    parent_dir = os.getcwd()
    playlist_dir = os.path.join(parent_dir, playlist_dir_name)
    os.mkdir(playlist_dir)
# Error catch to see if file directory exists
except FileExistsError:
    print("Directory exists...\nWriting to existing directory...")

# Changes working dir to newly made directory
os.chdir(playlist_dir)

# Initiates the download
downloadVideo(args.playlist)
