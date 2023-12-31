import typing as t
from .params import get_config
import asyncio
from operator import attrgetter
import pandas as pd 
import os 


__all__ = [
    "CollectSearch"
]

class CollectSearch:
    def __init__(
        self, 
        client, 
        query:str, 
        base_path:str, 
    ):
        self.query = query
        self.client = client
        self.base_path = base_path
    
    # search_albums
    # search_playlists
    # search_users
    # search_tracks
    
    async def get_data(self):
        return await asyncio.gather(
            self.get_recent_tracks()
        )
        