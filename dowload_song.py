from pytube import YouTube
import os

def downloadMP3(videoid: str)-> str:
    try:
        filePath = os.getcwd() + "/songs/"
        if os.path.exists(filePath + videoid + ".webm"):
                return(filePath + videoid + ".webm")
        video = YouTube("https://music.youtube.com/watch?v=" + videoid)

        streams = video.streams.filter(only_audio=True)
        # Find the stream with the highest bitrate but less than 280kbps
        filtered_streams = [stream for stream in streams if get_bitrate(stream) < 280]
        stream256kbps = max(filtered_streams, key=get_bitrate)
        out_path = stream256kbps.download(filePath)
        new_name = filePath + videoid + ".webm"
        os.rename(out_path, new_name)
        return new_name
    except Exception as e:
        pass
    return None

def get_bitrate(stream):
    return int(stream.abr[:-4])  # Convert '48kbps' to 48
        





