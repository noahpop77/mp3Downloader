#!/usr/bin/env python3
from __future__ import unicode_literals
from datetime import date
import pwd
import youtube_dl
import yt_dlp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import os
from datetime import date
import shutil
import sys
import json
import colorama
from colorama import Fore

# Playlist link passed in
PLAYLIST = sys.argv[1]
#PLAYLIST = "https://www.youtube.com/playlist?list=PLDWJwqI-7Ru-7pjP3k6zKkPbuAYzJ0ZyT"

# Video download function
def downloadVideo(inlink):
    ydl_opts = {    # Options for download
        'format': 'bestaudio/best',
        'ignoreerrors': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(inlink)

# Options for webdriver
options = webdriver.ChromeOptions()
options = Options()
options.headless = True
# Webdriver setup. Uses chrome driver manager service now instead of chromedriver exe
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
# Link that is passed to webdriver
print(f"\033[1;36mDownloading from:\033[0;0m {PLAYLIST}")
driver.get(PLAYLIST)

# Filters whole page for all 'a' tags
tagLinks = driver.find_elements(By.TAG_NAME, 'a')

# Loops through all 'a' tags in tagLinks and gets the href attribute
# Compares that to a regex pattern to get all video links specifically (and not random page links)
# Appends the links
links = []
for link in tagLinks:
    href = str(link.get_attribute('href'))
    if re.match(r".*watch.*", href ):
        links.append(link.get_attribute('href'))
removeDoops = list(dict.fromkeys(links))    # Removes duplicate entities

# Further santizes data
indexes = []
for index in removeDoops:
    if re.match(r".*index.*", index ):
        indexes.append(index)

# Get element with tag name 'div'
# Get all the elements available with tag name 'yt-formatted-string'
element = driver.find_element(By.TAG_NAME, 'body')
elements = element.find_elements(By.TAG_NAME, 'yt-formatted-string')

# Gets playlist title
title = ""
# Sets an iterator for the list of strings from the page
iterElements = iter(elements)
# Loops through all elements to find specifier for title
try: 
    while True:
        item = next(iterElements)
        if item.text == "PLAY ALL":
            item = next(iterElements)
            title = item.text
            break
except(StopIteration):
    print("Nothing Found....")
    print("The playlist may be private.")
    exit(0)

print(f"\033[1;36mDOWNLOADING PLAYLIST: {title}...\033[0;0m")

directory = f"{title} {date.today()}"       # Directory
parent_dir = "./"                           # Parent Directory path
path = os.path.join(parent_dir, directory)  # Path

# Create the directory, Catches exception if directory exists
try:
    os.mkdir(path)
    print("New directory made")
except(FileExistsError):
    print("File exists, continuing with execution...")

# Change working directory to new song folder
os.chdir(path)

# Playlist dictionary of current playlist data
playlists = {
    'playlists' : [
        {
            'name' : title,
            'link' : sys.argv[1],
            'length' : len(indexes)
        }
    ]
}

data = {}

try:
    with open('playlists.json', 'r') as json_playlist:
        data = json.load(json_playlist)
    json_playlist.close()
    with open('playlists.json', 'w') as json_playlist:

        oldLength = data['playlists'][0]['length']

        if oldLength != len(indexes):
            print("\033[1;36mDownloading playlist to Existing folder...\033[0;0m\n")
            downloadVideo(indexes[1])
        else:
            print("\033[1;31mNo Updates... Nothing downloaded...\033[0;0m\n")
        
        data['playlists'][0]['length'] = len(indexes)
        json.dump(data, json_playlist)

except:
    with open('playlists.json', 'w') as json_playlist:
        json.dump(playlists, json_playlist)
        print("\t\033[1;36mDownloading playlist to new folder...\n\033[0;0m")
        downloadVideo(indexes[1])


print("\033[1;36mSong Playlist:\033[0;0m")
for i in os.listdir("."):
    if re.match(r".*.mp3", i):
        print(i)

# Closes driver for cleanup
driver.quit()