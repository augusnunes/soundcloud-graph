import typing as t
from utils import get_scrap_features
import asyncio
from operator import itemgetter
import pandas as pd 
import os 

features = get_scrap_features()

class CollectTrack:
    def __init__(
        self, 
        client, 
        track_id:str, 
        base_path:str, 
    ):
        
        self.track_id = track_id
        self.base_path = base_path
        self.client = client
        self.map_of_func = {
            "albums": [self.client.get_track_albums, "album", "albums"],
            "playlists": [self.client.get_track_playlists, "playlist", "playlists"],
            "comments": [self.client.get_track_comments, "comment", "comments"],
            "likers": [self.client.get_track_likers, "user", "likers"],
            "reposters": [self.client.get_track_reposters, "user", "reposters"],
        }
    
    async def get_(self, func, type_of_columns, dir):
        list_of_elements = await list(func(self.track_id))
        pd.DataFrame(
            [list(itemgetter(*features[type_of_columns]["list_columns"])(element.__dict__)) for element in list_of_elements],
            columns=features[type_of_columns]["list_columns"],
        ).to_csv(os.path.join(self.base_path, dir, f"{self.track_id}.csv"), index=False)

    
    async def get_data(self, *string_functions, all_data:bool=False):
        if all_data:
            return await asyncio.gather(
                *[
                    self.get_(*self.map_of_func[i]) for i in self.map_of_func.keys()
                ]
            )
        if string_functions == ():
            return 
        return await asyncio.gather(
            *[
                self.get_(*self.map_of_func[i]) for i in string_functions
            ]
        )