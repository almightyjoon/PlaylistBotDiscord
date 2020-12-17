import discord
import json
import requests

from discord.ext import commands
from discord.utils import get
from secrets import spotify_token, spotify_user_id, playlist_id

# channel id is different for each channel
# secrets.py contains OAuth token, user id, playlist id for pl to add songs to
# client_secrets.json contains client id and client secret


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    # detects for reactions on a message in channel "music-sharing"
    # if 2 ❤ reactions are detected then add to playlist
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        # replace CHANNEL_ID_HERE with channel id for the channel the bot will be used for
        if payload.channel_id == "CHANNEL_ID_HERE" and payload.emoji.name == "❤️":
            channel = self.client.get_channel("CHANNEL_ID_HERE")
            message = await channel.fetch_message(payload.message_id)
            if message.author.bot:
                return
            else:
                reaction = get(message.reactions, emoji=payload.emoji.name)
                if reaction and reaction.count > 1:
                    await message.channel.send(f">>Received 2+ votes, song added to playlist: '{message.content}'")
                    ctx = await self.client.get_context(message)
                    uri = await ctx.invoke(self.client.get_command('get_uri_from_url'), message.content)
                    await ctx.invoke(self.client.get_command('add_to_playlist'), uri)

    @commands.command(aliases=['geturifromurl'])
    async def get_uri_from_url(self, ctx, url):
        # slice url to get "spotify"
        is_spotify = url.split('.')

        # slice the_rest to get "artist/track/album/playlist/user"
        identifier = is_spotify[2].split('/')

        # slice more_of_the_rest to get spotify id
        spotify_id = identifier[2].split('?')

        # format string to get the spotify uri for url
        spotify_uri = is_spotify[1] + ':' + identifier[1] + ':' + spotify_id[0]
        return spotify_uri

    @commands.command(aliases=['addtoplaylist'])
    async def add_to_playlist(self, ctx, uri):
        request_data = json.dumps(uri)
        query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={uri}"

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {spotify_token}"
            }
        )

        response_json = response.json()
        return response_json


def setup(client):
    client.add_cog(Music(client))
