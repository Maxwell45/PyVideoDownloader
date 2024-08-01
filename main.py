import shutil
from collections.abc import Iterable

from time import sleep

from pytube import YouTube as yt
from pytube import Playlist as pl

import re
import os

defpath: str = "D:\\downloads"
version: str = "1.2"

def get_size(o):
    s = 0
    for _ in o:
        s += 1
    return s


def remake_dir(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)
    os.chdir(path)


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
            if video_resolutions.count(r) == 0:
                resolutions.remove(r)
                if get_size(resolutions) == 0:
                    return None
    return resolutions


def remove_all(string: str):
    characters_to_delete = ["\\", "/", ".", "\"", ":", ",", "?", "'"]
    for c in characters_to_delete:
        string = string.replace(c, "")
    return string


def download(video: yt, audio_only: bool, resolution: str):
    title = video.title
    title = remove_all(title)
    if video.streams.get_by_resolution(resolution) is None:
        print(title + " does not have the specified resolution available. Skipping...")
        return
    print("Downloading " + title)
    path: str = os.getcwd()
    while True:
        try:
            if audio_only:
                video.streams.get_audio_only().download(path, title + ".mp3")
            else:
                video.streams.get_by_resolution(resolution).download(path, title + ".mp4")
            print("Download successful")
            break

        except RuntimeError as e:
            sleep(10)
            print("Failed to download " + title + ", retrying...")
            continue


def main():
    print("Welcome to Max's YT downloader version " + version)
    if not os.path.isdir(defpath):
        os.makedirs(defpath)
    url = input("Paste the video or playlist URL here: ")

    while True:
        audio_prompt = input("Download audio only? ").lower()
        if audio_prompt == "y" or audio_prompt == "n":
            break

    audio_only = (audio_prompt == "y")

    resolution = ""

    is_list = (re.search("list=", url) is not None)

    if is_list:
        playlist = pl(url)
        folder_name: str = remove_all(playlist.title)
        if not audio_only:
            remake_dir(defpath + "/mp4/" + folder_name)
            print("Fetching available resolutions on all videos...")
            resolutions = get_common_resolutions(playlist.videos)
            print("Available resolutions are: " + str(resolutions))
            resolution = input("Please select your desired resolution: ")
        else:
            remake_dir(defpath + "/mp3/" + folder_name)
        size = get_size(playlist.videos)
        for i in range(0, size - 1):
            video: yt = playlist.videos[i]
            video.use_oauth = True
            video.allow_oauth_cache = True
            print("Downloading video " + str(i + 1) + " out of " + str(size - 1))
            download(video, audio_only, resolution)

    else:
        video = yt(url, use_oauth=True, allow_oauth_cache=True)
        if not audio_only:
            if not os.path.isdir(defpath + "/mp4/Singles"):
                os.makedirs(defpath + "/mp4/Singles")
            os.chdir(defpath + "/mp4/Singles")
            print("Fetching available resolutions for the video...")
            resolutions = get_resolutions(video)
            print("Available resolutions are: " + str(resolutions))
            resolution = input("Please select your desired resolution: ")
        else:
            if not os.path.isdir(defpath + "/mp3/Singles"):
                os.makedirs(defpath + "/mp3/Singles")
            os.chdir(defpath + "/mp3/Singles")
        video: yt = yt(url)
        video.use_oauth = True
        video.allow_oauth_cache = True
        download(video, audio_only, resolution)


if __name__ == '__main__':
    main()
