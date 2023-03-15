from pytube import YouTube as yt


def download(link, res, audio):
    youtube_object = yt(link)
    if audio:
        youtube_object = youtube_object.streams.get_audio_only("mp3")
    else:
        youtube_object = youtube_object.streams.get_by_resolution(res)
    try:
        youtube_object.download("D:\\downloads\\", None, None, False, 10, 5)
        print("Download is completed successfully")
    except:
        print("An error has occurred, check URL or the quality resolution")


video_url = input("Enter the YouTube video URL: ")
while True:
    audio_only = input("Download audio only? y/n: ")
    audio_only = audio_only.lower()
    if audio_only == "y":
        print("Downloading the video")
        download(video_url, None, True)
        break
    if audio_only == "n":
        resolution = input("Enter the resolution: ")
        print("Downloading the video")
        download(video_url, resolution, False)
        break
