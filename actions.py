import discord
from urllib.parse import quote, unquote_plus
import queue_manager
from discord.ui import View
import asyncio
import os
import song_manager

last_button_msg = {}
last_embed = {}
in_loop = {}

class Song_btns(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(emoji= "⏸", custom_id="play_pause_button", style= discord.ButtonStyle.grey)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        pass
    @discord.ui.button(emoji= "⏩", custom_id="next_button", style= discord.ButtonStyle.grey)
    async def button_callback2(self, interaction: discord.Interaction, button: discord.ui.button):
        pass
    @discord.ui.button(emoji= "🔁", custom_id="loop_button", style= discord.ButtonStyle.grey)
    async def button_callback3(self, interaction: discord.Interaction, button: discord.ui.button):
        pass
    @discord.ui.button(emoji= "❌", custom_id="stop_button", style= discord.ButtonStyle.grey)
    async def button_callback4(self, interaction: discord.Interaction, button: discord.ui.button):
        pass


class Actions():

    async def play(self, channel,interaction: discord.Interaction, songUrl, video_id, song_name, artist, thumbnail, voice_channel, author_name,):
        guild_id = interaction.guild_id
        voice_channel.play(discord.FFmpegPCMAudio(songUrl,), after=lambda e: print(e))
        embed = discord.Embed(title=f"Song name : {unquote_plus(song_name)}", color= 21643, description = f"By {unquote_plus(artist)}", url= "https://www.instagram.com/hackticaayush")
        #embed.set_image(url= "https://d3k81ch9hvuctc.cloudfront.net/company/UNatcp/images/1cf2cb0e-dddb-4d51-8878-191e0798c4fa.gif")
        embed.set_footer(text= "PLAYING...  ♫ ♪", icon_url= "https://media.tenor.com/15YUsMWt4FEAAAAj/music.gif")
        embed.set_thumbnail(url=unquote_plus(thumbnail))
        view = Song_btns()
        if in_loop[guild_id] == True:
            view.children[2].emoji = "🔂"
        wbhook1 = await channel.send(embed=embed, view=view)
        loop_emoji = wbhook1.components.copy()[0].children[2].emoji.name
        last_msg_id = last_button_msg.get(guild_id)
        if not last_msg_id == None:
            wbhook2 = await channel.fetch_message(last_msg_id)
            embed2 = last_embed.get(interaction.guild_id)
            embed2.set_footer(text= "FINISHED  ", icon_url= "https://media.tenor.com/15YUsMWt4FEAAAAj/music.gif")
            await wbhook2.edit(embed=embed2, view= None)
        last_button_msg[interaction.guild_id]= wbhook1.id
        last_embed[interaction.guild_id] = embed
        while voice_channel.is_playing() or voice_channel.is_paused():
            await asyncio.sleep(1)
        if not voice_channel.is_connected():
            return
        last_msg_id = last_button_msg.get(interaction.guild_id)
        last_button_msg[interaction.guild_id]
        if not last_msg_id == None:
            wbhook2 :discord.WebhookMessage
            wbhook2 = await channel.fetch_message(last_msg_id)
            embed.set_footer(text= "FINISHED  ", icon_url= "https://media.tenor.com/15YUsMWt4FEAAAAj/music.gif")
        await wbhook2.edit(embed=embed, view= None)
        await self.on_finished(guild_id=guild_id, video_id=video_id, channel=channel, interaction=interaction, voice_channel=voice_channel)


    async def on_finished(self, guild_id, video_id, channel, interaction: discord.Interaction, voice_channel):
        if len(queue_manager.get_all_queue(guild_id=guild_id)) >= 1 and in_loop[guild_id] == False:
            queue_manager.delete_finished_data(video_id=video_id, guild_id=guild_id)
        if len(queue_manager.get_all_queue(guild_id=guild_id)) == 0:
            await voice_channel.disconnect()
            return
        new_video_id = queue_manager.get_all_queue(guild_id=guild_id)[0]
        songUrl = os.getcwd() + "/songs/" + new_video_id + ".webm"
        new_song_data = song_manager.get_song_data(new_video_id)
        song_name = quote(new_song_data.get('song_name'))
        artist = quote(new_song_data.get('artist'))
        thumbnail = new_song_data.get('thumbnail')
        await self.play(
            channel=channel, interaction=interaction, songUrl=songUrl, video_id=new_video_id, song_name=song_name,
            artist=artist, thumbnail=thumbnail, voice_channel=voice_channel, author_name= None
        )


    @staticmethod
    async def pause(channel, voice_channel, interaction: discord.Interaction):
        last_msg_id = last_button_msg.get(interaction.guild_id)
        if not last_msg_id == interaction.message.id:
            await interaction.message.delete()
            return
        if not voice_channel == None:
            voice_channel.pause()
        message_id = interaction.message.id
        message = await channel.fetch_message(message_id)
        embed = interaction.message.embeds.copy()[0].set_footer(text= "PAUSED  ♫ ♪", icon_url= "https://media.tenor.com/15YUsMWt4FEAAAAj/music.gif")
        view = Song_btns()
        view.children[0].emoji = "▶️"
        view.children[0].style = discord.ButtonStyle.grey
        await message.edit(embed=embed, view=view)
        await interaction.response.defer()

    @staticmethod
    async def resume(channel, voice_channel, interaction: discord.Interaction):
        last_msg_id = last_button_msg.get(interaction.guild_id)
        if not last_msg_id == interaction.message.id:
            await interaction.message.delete()
            return
        if not voice_channel == None:
            voice_channel.resume()
        message_id = interaction.message.id
        message = await channel.fetch_message(message_id)
        embed = interaction.message.embeds.copy()[0].set_footer(text= "PLAYING...  ♫ ♪", icon_url= "https://media.tenor.com/15YUsMWt4FEAAAAj/music.gif")
        view = Song_btns()
        await message.edit(embed=embed, view=view)
        await interaction.response.defer()

    @staticmethod
    async def stop(channel, voice_channel, interaction: discord.Interaction):
        last_msg_id = last_button_msg.get(interaction.guild_id)
        if not last_msg_id == interaction.message.id:
            await interaction.message.delete()
            return
        if not voice_channel == None:
            await voice_channel.disconnect()
        queue_manager.clear_all_queue(interaction.guild_id)
        message_id = interaction.message.id
        message = await channel.fetch_message(message_id)
        embed = interaction.message.embeds.copy()[0].set_footer(text= "STOPED  ", icon_url= "https://media.tenor.com/15YUsMWt4FEAAAAj/music.gif")
        await message.edit(embed=embed, view=None)
        await interaction.response.defer()

    @staticmethod
    async def next(channel, voice_channel, interaction: discord.Interaction):
        last_msg_id = last_button_msg.get(interaction.guild_id)
        if not last_msg_id == interaction.message.id:
            await interaction.message.delete()
            return
        else:
            voice_channel.stop()

    @staticmethod
    async def loop(channel, voice_channel, interaction: discord.Interaction):
        last_msg_id = last_button_msg.get(interaction.guild_id)
        if not last_msg_id == interaction.message.id:
            await interaction.message.delete()
            return None
        else:
            emo = interaction.message.components.copy()[0].children[2].emoji.name
            emoji1 = interaction.message.components.copy()[0].children[0].emoji.name
            if queue_manager.insert_at_one(guild_id=interaction.guild_id, in_loop=in_loop) :
                emoji2 = "🔁"
            else:
                emoji2 = "🔂"
            if emo == emoji2:
                if emo == "🔁":
                    emoji2 = "🔂"
                else: emoji2 = "🔁"
            view = Song_btns()
            view.children[0].emoji = emoji1
            view.children[2].emoji = emoji2
            message = await channel.fetch_message(interaction.message.id)
            await message.edit(view=view)
            if emoji2 == "🔂":
                in_loop[interaction.guild_id] = True
            else:
                in_loop[interaction.guild_id] = False
            await interaction.response.defer()