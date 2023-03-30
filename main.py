from pytube import YouTube as yt, StreamQuery, Stream


def progress_function(stream, chunk, bytes_remaining):
    size = stream.filesize
    p = percent(bytes_remaining, size)
    print(str(p) + '%')


def percent(tem, total):
    perc = (float(tem) / float(total)) * float(100)
    return perc


def download(link, res, audio):
    youtube_object = yt(link, on_progress_callback=progress_function())
    if audio:
        download_stream: Stream = youtube_object.streams.get_audio_only("mp3").first()
    else:
        download_stream: Stream = youtube_object.streams.filter(resolution=res).first()
    download_stream.download("D:\\downloads\\", None, None, False, 10, 5)
    print("Download is completed successfully")


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
