from ytmusicapi import YTMusic, OAuthCredentials, setup_oauth
import json
from dotenv import load_dotenv
import os
import requests
import functools
from langchain.agents import Tool
from typing import Annotated
from langchain.tools import StructuredTool

load_dotenv(override=True)

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

class NotAuthenticated:
    def __init__(self):
        self.yt = YTMusic()

    def search_song(self, song_name):
        search_results = self.yt.search(song_name)
        songs = []
        for item in search_results:
            if item.get("resultType") == "song":
                album_info = item.get("album")
                album_name = album_info.get("name", "") if isinstance(album_info, dict) else ""
                
                song_entry = {
                    "song_id": item.get("videoId", ""),  # renamed from videoId
                    "title": item.get("title", ""),
                    "duration": item.get("duration", ""),
                    "artists": [a["name"] for a in item.get("artists", [])] if isinstance(item.get("artists"), list) else [],
                    "album": album_name,
                }
                songs.append(song_entry)
        return songs

class Authenticated:
    s = requests.Session()
    s.request = functools.partial(s.request, timeout=60)
    def __init__(self):
        #self.yt = YTMusic(oauth_credentials=OAuthCredentials(client_id=GOOGLE_CLIENT_ID, client_secret=GOOGLE_CLIENT_SECRET))
        self.yt = YTMusic("browser.json")
        print(self.yt)
    
    def get_user_library(self, user = None):
        user_playlist = self.yt.get_library_playlists()
        # Parse and clean data
        parsed_playlists = []
        for pl in user_playlist:
            parsed = {
                "title": pl.get("title"),
                "playlistId": pl.get("playlistId"),
                "description": pl.get("description"),
                "track_count": pl.get("count", None),
                #"author": pl.get("author", [{}])[0].get("name") if "author" in pl else None,
                #"largest_thumbnail": max(pl.get("thumbnails", []), key=lambda t: t["width"])["url"] if pl.get("thumbnails") else None
            }
            parsed_playlists.append(parsed)

        # Output as JSON string
        json_output = json.dumps(parsed_playlists, indent=4)
        print(json_output)

        # Or save to a file
        with open("playlists.json", "w", encoding="utf-8") as f:
            f.write(json_output)

        return json_output
    
    def get_playlist(self, playlist_id = 'PLZnYAMmCI5BY7zF-ShOUWie2qHgWuXQHo'):
        playlist_data = self.yt.get_playlist(playlistId=playlist_id)
        return playlist_data
    
    def search_autenticated(self, query):
        search_results = self.yt.search(query)
        songs = []
        for item in search_results:
            if item.get("resultType") == "song":
                album_info = item.get("album")
                album_name = album_info.get("name", "") if isinstance(album_info, dict) else ""
                
                song_entry = {
                    "song_id": item.get("videoId", ""),
                    "title": item.get("title", ""),
                    "duration": item.get("duration", ""),
                    "artists": [a["name"] for a in item.get("artists", [])] if isinstance(item.get("artists"), list) else [],
                    "album": album_name,
                }
                songs.append(song_entry)
        return songs
    
    def add_song_to_playlist(self, playlist_id: str, song_id: list[str]):
        """
        Use this tool to add songs to a YouTube Music playlist.

        Parameters:
            playlist_id (str): The ID of the playlist where songs should be added.
            song_id (list[str]): A list of song IDs (videoIds) to add. 
                                You can pass one or multiple IDs.

        Returns:
            dict: A response from YouTube Music API containing:
                - status: "STATUS_SUCCEEDED" if successful
                - setVideoId: mapping of added videoIds
                - or error details if failed
        """
        return self.yt.add_playlist_items(
            playlistId=playlist_id,
            videoIds=song_id
        )
    
    def create_new_playlist(self, playlist_name : str, playlist_description : str, song_id : list):
        """use this tool to add songs to the playlist. pass a playlist name and its description. also pass the song id to add to the playlist"""
        create_playlist = self.yt.create_playlist(title=playlist_name, description=playlist_description, video_ids=song_id)
        return create_playlist
    



    def get_yt_tools(self):
        get_lib_playlist = Tool(
            name = 'get_lib_playlist',
            description= ' use this tool to get all the playlist user currently has in their library. note the user is already authenticated. just pass a dummy user id to the function',
            func= self.get_user_library
        )
        yt_search = Tool(
            name = 'youtube_music_search',
            description= 'use this tool to search songs from youtube music',
            func=self.search_autenticated
        )

        add_to_playlist = StructuredTool.from_function(
        name = 'add_to_playlist',
        description= 'use this tool to add a song to user playlist. you need to pass the playlist id and the song id or video id to the tool',
        func= self.add_song_to_playlist
        )

        create_playlist = StructuredTool.from_function(
            name = 'create_playlist',
            description= 'use this tool to create a new playlist for the user in youtube music. you need to pass a playlist name (any name you like if user not mentioned a specific name), a playlist description and the id of the songs to be added to the new playlist',
            func= self.create_new_playlist
        )

        return [get_lib_playlist, yt_search, add_to_playlist,create_playlist]









