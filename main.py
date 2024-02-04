from time import sleep

from pytubefix import YouTube as yt
from pytubefix import Playlist as pl
import re


def get_size(o):
    s = 0
    for _ in o:
        s += 1
    return s


def download(video, audio_only, quality):
    if video.streams.get_by_resolution(quality) is None:
        print(video.title + " does not have the specified resolution available. Skipping...")
        return
    print("Downloading " + video.title)
    while True:
        try:
            if audio_only:
                video.streams.get_audio_only().download(path)
            else:
                video.streams.get_by_resolution(quality).download(path)
            print("Download successful")
            break
        except:
            sleep(10)
            print("Failed to download " + video.title + ", retrying...")
            continue


path = "D:\\downloads"
url = input("Paste the video or playlist URL here: ")
audio_only = None
while audio_only != "y" and audio_only != "n":
    audio_only = input("Download audio only? ").lower()
    if audio_only == "y":
        audio_only = True
        break
    if audio_only == "n":
        audio_only = False
        break

quality = ""

if not audio_only:
    quality = input("Please select your desired quality: ")

if re.search("list=", url) is not None:
    playlist = pl(url)
    size = get_size(playlist.videos)
    for i in range(0, size - 1):
        video = playlist.videos[i]
        print("Downloading video " + str(i + 1) + " out of " + str(size - 1))
        download(video, audio_only, quality)


else:
    video = yt(url)
    download(video, audio_only, quality)
