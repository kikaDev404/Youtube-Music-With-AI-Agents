import asyncio
from langchain.agents import Tool
from yt_music import NotAuthenticated as yt

yt_music = yt()

search_tool = Tool(
    name="search_music",
    description="use this tool to search for a song on YouTube Music",
    func=yt_music.search_song  # async function
)

print(search_tool.invoke('eminem'))
