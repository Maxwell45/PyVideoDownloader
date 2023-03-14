from pytube import YouTube


def download(link, res):
    youtube_object = YouTube(link)
    youtube_object = youtube_object.streams.get_by_resolution(res)
    try:
        youtube_object.download()
    except:
        print("An error has occurred, check URL or the quality resolution")
    print("Download is completed successfully")


videoURL = input("Enter the YouTube video URL: ")
resolution = input("Enter the resolution: ")
print("Downloading the video")
download(videoURL, resolution)
