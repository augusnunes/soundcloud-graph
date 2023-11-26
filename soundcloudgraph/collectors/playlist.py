import typing as t
from .params import get_config
import asyncio
from operator import attrgetter
import pandas as pd 
import os 
from soundcloud.resource.track import BasicTrack


class CollectPlaylist:
    def __init__(
        self, 
        client, 
        playlist_id:str, 
        base_path:str, 
    ):
        self.playlist_id = playlist_id
        self.base_path = base_path
        self.client = client
        self.map_of_func = {
            "likers": [self.client.get_playlist_likers, "user", "likers"],
            "reposters": [self.client.get_playlist_reposters, "user", "reposters"],
            "tracks": self.get_tracks
        }
        for i in self.map_of_func.keys():
            os.makedirs(
                os.path.join(
                    self.base_path,
                    i
                )
            )
    
    async def get_(self, func, type_of_columns, dir):
        list_of_elements = await list(func(self.playlist_id))
        pd.DataFrame(
            [list(attrgetter(*get_config()[type_of_columns])(element.__dict__)) for element in list_of_elements],
            columns=get_config()[type_of_columns],
        ).to_csv(os.path.join(self.base_path, dir, f"{self.playlist_id}.csv"), index=False)

    async def get_tracks(self):
        list_of_tracks = self.client.get_playlist(self.playlist_id).tracks
        pd.DataFrame(
            [list(attrgetter(*get_config()["track"])(track.__dict__)) for track in list_of_tracks if isinstance(track, BasicTrack)]
        ).to_csv(os.path.join(self.base_path, "tracks", f"{self.playlist_id}.csv"), index=False)
        
    async def get_data(self, *string_functions):
        if string_functions == ():
            return await asyncio.gather(
                *[
                    self.get_(*self.map_of_func[i]) if i != "tracks" else self.map_of_func["tracks"]() for i in self.map_of_func.keys() 
                ]
            ) 
        return await asyncio.gather(
            *[
                self.get_(*self.map_of_func[i]) if i != "tracks" else self.map_of_func["tracks"]() for i in string_functions
            ]
        )