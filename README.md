# PlaylistBotDiscord

This is a bot that can be added to a specific channel in your Discord server to grab a Spotify URL that was shared and add the song to a designated playlist.
The song must receive 2(number can be changed) or more ❤️reactions to be added to the playlist.

In secrets.py, user is required to fill in their corresponding OAuth token, Spotify user id, and the Playlist ID for the playlist you wish to add your songs to.
https://developer.spotify.com/console/post-playlists/

In client_secrets.json, fill in client_id and client_secrets. 
https://developer.spotify.com/dashboard/applications

In music.py in cogs, CHANNEL_ID_HERE must be replaced by the channel ID for the channel that you wish for the bot to pull reaction data from.
Reaction emoji is default set to ❤️, but can be replaced with any valid emoji.
