import discord
from discord.interactions import Interaction

async def create_channel(interaction: Interaction, channel_name: str):
    await interaction.guild.create_voice_channel(name = channel_name)

def get_voice_channels_list(interaction: Interaction):
    voice_channel_list = interaction.guild.voice_channels
    return voice_channel_list

def get_voice_channels_names(voice_channel_list):
    channel_names = []
    for channel in voice_channel_list:
        channel_names.append(channel.name)
    return channel_names

def is_bot_channel_exist(interaction: Interaction, channel_name: str) -> bool:
    voice_channel_list = get_voice_channels_list(interaction = interaction)
    voice_channel_names = get_voice_channels_names(voice_channel_list= voice_channel_list)
    if not voice_channel_names.__contains__(channel_name):
        return False
    else:
        return True
    
def get_bot_channel(interaction: Interaction, channel_name: str):
    channel = discord.utils.get(get_voice_channels_list(interaction= interaction), name= channel_name)
    return channel
    
async def set_voice_channel_config(interaction: Interaction, channel_name: str) -> bool:
    channel_exists = is_bot_channel_exist(interaction= interaction, channel_name= channel_name)
    if not channel_exists:
        try:
            channel = await create_channel(interaction= interaction, channel_name= channel_name)
            return True
        except Exception as e:
            print(f"Error in channel creation: {e}")
            return False
    else:
        return True