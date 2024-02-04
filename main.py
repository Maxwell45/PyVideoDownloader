from collections.abc import Iterable
from time import sleep

from pytubefix import YouTube as yt
from pytubefix import Playlist as pl
import re


def get_size(o):
    s = 0
    for _ in o:
        s += 1
    return s


def get_resolutions(video: yt):
    presets = ["144p", "240p", "360p", "480p", "720p", "1080p"]
    resolutions = []

    for p in presets:
        stream = video.streams.get_by_resolution(p)
        if stream is not None:
            resolutions.append(stream.resolution)
    return resolutions


def get_common_resolutions(videos: Iterable[yt]):
    resolutions = ["144p", "240p", "360p", "480p", "720p", "1080p"]
    for v in videos:
        video_resolutions = get_resolutions(v)
        for r in resolutions:
            if (video_resolutions.count(r) == 0):
                resolutions.remove(r)
                if (get_size(resolutions) == 0):
                    return None
    return resolutions


def download(video: yt, audio_only: bool, resolution: str):
    if video.streams.get_by_resolution(resolution) is None:
        print(video.title + " does not have the specified resolution available. Skipping...")
        return
    print("Downloading " + video.title)
    while True:
        try:
            if audio_only:
                video.streams.get_audio_only().download(path)
            else:
                video.streams.get_by_resolution(resolution).download(path)
            print("Download successful")
            break
        except:
            sleep(10)
            print("Failed to download " + video.title + ", retrying...")
            continue


path = "D:\\downloads"

url = input("Paste the video or playlist URL here: ")

audio_only = None
audio_prompt = ""

while True:
    audio_prompt = input("Download audio only? ").lower()
    if audio_prompt == "y" or audio_prompt == "n":
        break

audio_only = (audio_prompt == "y")

resolution = ""

is_list = (re.search("list=", url) is not None)

if is_list:
    playlist = pl(url)
    if not audio_only:
        print("Fetching available resolutions on all videos...")
        resolutions = get_common_resolutions(playlist.videos)
        print("Available resolutions are: " + str(resolutions))
        resolution = input("Please select your desired resolution: ")

    size = get_size(playlist.videos)
    for i in range(0, size - 1):
        video = playlist.videos[i]
        print("Downloading video " + str(i + 1) + " out of " + str(size - 1))
        download(video, audio_only, resolution)

else:
    video = yt(url)
    if not audio_only:
        print("Fetching available resolution for the video...")
        resolutions = get_resolutions(video)
        print("Available resolutions are: " + str(resolutions))
        resolution = input("Please select your desired resolution: ")
    video = yt(url)
    download(video, audio_only, resolution)