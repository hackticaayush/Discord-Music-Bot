import functools


song_data = {}

def add_song_data(video_id, song_name, artist, thumbnail):
    song_data[video_id] = {
        "song_name": song_name,
        "artist": artist,
        "thumbnail": thumbnail,
    }

def delete_song_data(video_id):
    if video_id in song_data:
        del song_data[video_id]


@functools.lru_cache(maxsize=500)
def get_song_data(video_id):
    return song_data.get(video_id)
