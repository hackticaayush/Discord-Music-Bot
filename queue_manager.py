import functools
import os
import shutil


queue_data = {}

def add_queue_data(video_id, guild_id):
    if guild_id not in queue_data:
        queue_data[guild_id] = []

    if len(queue_data[guild_id]) >= 15:
        oldest_video_id = next(iter(queue_data[guild_id])) # Remove the oldest video ID to make room for the new one
        del queue_data[guild_id][oldest_video_id]
        try:
            filePath = os.getcwd() + "/songs/" + oldest_video_id + ".webm"
            if os.path.exists(filePath):
                shutil.rmtree(filePath)
        except Exception as e:
            print(f"Error: {e}")

    queue_data[guild_id].append(video_id)

def delete_finished_data(video_id, guild_id):
        del queue_data[guild_id][0]

def get_all_queue(guild_id):
    return queue_data[guild_id]

def clear_all_queue(guild_id):
    queue_data[guild_id]= []
    
def insert_at_one(guild_id, in_loop):
    video_id = queue_data[guild_id][0]
    if len(queue_data[guild_id]) > 1:
        if queue_data[guild_id][1] == video_id and in_loop[guild_id] == True:
            queue_data[guild_id].pop(1)
            return False
    else:
        queue_data[guild_id].insert(1, video_id)
        return True

@functools.lru_cache(maxsize=10)
def get_queue_data(video_id, guild_id):
    return queue_data.get(guild_id, {}).get(video_id, {})
