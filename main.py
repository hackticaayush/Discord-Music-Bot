import settings
import discord
from discord.ext import commands
from typing import Optional
from discord.ext import commands
from discord import app_commands
import dowload_song
import search_song
import json
from urllib.parse import quote, unquote, unquote_plus
from discord.ui import View
import nacl
import sys
import queue_manager
import song_manager
from actions import Actions, in_loop, last_button_msg, last_embed
from voice_channel import set_voice_channel_config, get_bot_channel


def run():
    bot = commands.Bot(command_prefix="!", intents= discord.Intents.default())
    intents = discord.Intents.default()
    intents.members = True
    intents.messages = True
    intents.message_content

    
    try:
        discord.opus.load_opus(f"{settings.work_dir}/libs/{settings.libopus_build_file_name}")
    except Exception as e:
        print(f"Error while loading libopus file : {e}")
    if discord.opus.is_loaded():
        print("libopus loaded succesfully")
    else:
        sys.exit(1)


    @bot.event
    async def on_ready():
        print("---------------------------------")
        print(f'bot >> {bot.user}')
        print(f'bot userID >> {bot.user.id}')
        print(f'{bot.user.name} is ready to rock🎤')
        print("---------------------------------\n")
        await bot.tree.sync()


    @bot.command()
    async def ping(ctx):
        await ctx.author.send("pong")


    actions = Actions()


    class btn_callback():
        @staticmethod
        async def play_pause(interaction: discord.Interaction):
            interaction_channel = interaction.channel
            bot_voice_channel_id = get_bot_channel(interaction=interaction, channel_name= "Musically").id
            voice_channel = discord.utils.get(bot.voice_clients, channel__id=bot_voice_channel_id)
            if not voice_channel == None:
                if voice_channel.is_playing():
                    await actions.pause(interaction_channel,voice_channel, interaction)
                elif voice_channel.is_paused():
                    await actions.resume(interaction_channel,voice_channel, interaction)
            else:
                await interaction.message.delete()



            

    @bot.event
    async def on_interaction(interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component:
            channel = interaction.channel
            bot_voice_channel_id = get_bot_channel(interaction= interaction, channel_name= "Musically").id
            voice_channel = discord.utils.get(bot.voice_clients, channel__id=bot_voice_channel_id)
            if interaction.data['custom_id'] == "play_pause_button":      
                await btn_callback.play_pause(interaction)
            elif interaction.data['custom_id'] == "stop_button":
                if not voice_channel == None:
                    await actions.stop(channel= channel, interaction= interaction, voice_channel= voice_channel)
                else:
                    await interaction.message.delete()
            elif interaction.data['custom_id'] == "next_button":
                if not voice_channel == None:
                    await actions.next(channel= channel, interaction= interaction, voice_channel= voice_channel)
                else:
                    await interaction.message.delete()
            elif interaction.data['custom_id'] == "loop_button":
                if not voice_channel == None:
                    await actions.loop(channel= channel, interaction= interaction, voice_channel= voice_channel)
                else:
                    await interaction.message.delete()      



    async def song_autocomplete(interaction: discord.Interaction, current: str) -> [app_commands.Choice[str]]: # type: ignore
        data = []
        if current == "":
            return data
        search_result = search_song.getResult(current.lower(), False)
        with open('songsData.json', 'w') as json_file:
            json_file.write('{}')
        val2 = []
        for result in search_result:
            result_dict = json.loads(result)
            song_name = unquote(result_dict['name'])
            if len(song_name) >= 31:
                song_name = song_name[:30]
            artist = unquote(result_dict['artist'])
            if len(artist) >= 36:
                artist = artist[:35]
            thumbnail = quote(result_dict['thumbnail'])
            video_id = result_dict['videoId']
            data.append(app_commands.Choice(name= song_name + " by " + artist, value= video_id))
            song_manager.add_song_data(video_id=video_id, song_name= song_name, artist= artist, thumbnail= thumbnail)
        return data 


    @bot.tree.command(name= "play", description="Search any song of your choice and play")
    @app_commands.autocomplete(song= song_autocomplete)
    async def play(interaction: discord.Interaction, song: str):
        bot_channel_name = "Musically"
        voice_channel_setup = await set_voice_channel_config(interaction= interaction, channel_name= bot_channel_name)
        if not voice_channel_setup:
            await interaction.response.send_message("Error in creating voice channel. Please give the required permission to the bot", ephemeral=True, delete_after=30)
        else:
            voice_channel = get_bot_channel(interaction= interaction, channel_name= bot_channel_name)
            voice_channel_id = voice_channel.id
            await interaction.response.send_message("Wait for few seconds, your song will be added in queue", ephemeral= True, delete_after= 7)
            channel = interaction.channel
            channel.typing()
            songUrl = dowload_song.downloadMP3(song)
            if songUrl is None:
                #here item is serch song if user dont choose any song from the list and send directly to the bot the song name then item is song name and we can use this to step1
                # to get the proper serch reasult from the website which is link of a yt video but we have to code here that what to send in embed
                await interaction.followup.send("Sorry, this song is not available to play.", ephemeral=True)
            else:
                author_name = interaction.user.display_name
                song_data = song_manager.get_song_data(song)
                song_name = song_data.get('song_name', '')
                await channel.send(f"{author_name} added {song_name} in queue.", suppress_embeds= True)
                artist = song_data.get('artist', '')
                thumbnail = song_data.get('thumbnail', '')
                connected_voice_channel = discord.utils.get(bot.voice_clients, channel__id=voice_channel_id)
                if connected_voice_channel is None:
                    connected_voice_channel = await voice_channel.connect(self_deaf= True)
                guild_id = interaction.guild_id
                queue_manager.add_queue_data(video_id=song, guild_id= guild_id)
                if connected_voice_channel.is_playing() or connected_voice_channel.is_paused():
                    pass
                else:
                    if connected_voice_channel.is_connected():
                        in_loop[guild_id] = False
                        await actions.play(channel=channel, songUrl=songUrl,interaction= interaction, video_id=song, song_name=song_name, artist= artist, thumbnail= thumbnail, voice_channel= connected_voice_channel, author_name=author_name,)


    bot.run(settings.DISCORD_BOT_TOKEN)
                        


if __name__ == "__main__":
    run()