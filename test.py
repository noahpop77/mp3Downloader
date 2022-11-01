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
                    help='Save location for songs')
parser.add_argument('--playlist',
                    help='Link to the playlist that will be downloaded')
args = parser.parse_args()
#args.playlist
#args.path


try:
    playlist_dir_name = args.path
    parent_dir = os.getcwd()
    playlist_dir = os.path.join(parent_dir, playlist_dir_name)
    os.mkdir(playlist_dir)
except FileExistsError:
    print("Directory exists...\nWriting to existing directory...")

os.chdir(playlist_dir)

downloadVideo(args.playlist)
