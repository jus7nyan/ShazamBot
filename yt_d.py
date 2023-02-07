import yt_dlp as ydlp


def yt_down(url, frmt, path,name):
    audio = ["mp3","audio"]
    video = ["mp4","video"]
    
    if frmt in audio:
        options = {"format": "bestaudio","extract_audio":True, "audio_format": "mp3","outtmpl":f"{path}{name}.mp3"}
        with ydlp.YoutubeDL(options) as ydl:
            ydl.download(url)
        return "mp3"

    elif frmt in video:
        options = {"format":"22", "outtmpl":f"{path}{name}.mp4"}
        with ydlp.YoutubeDL(options) as ydl:
            ydl.download(url)
        return "mp4"
    
    