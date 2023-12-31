import typing as t
from .params import get_config
import asyncio
from operator import attrgetter
import pandas as pd 
import os 


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
            "track_metadata": self.get_track_metadata,
        }
        for i in self.map_of_func.keys():
            if not os.path.exists(os.path.join(self.base_path,i)) and i != "track_metadata":
                os.makedirs(
                    os.path.join(
                        self.base_path,
                        i
                    )
                )
    
    async def get_track_metadata(self):
        df = pd.DataFrame(
            [list(attrgetter(*get_config()["track"])(self.client.get_track(self.track_id)))],
            columns = get_config()["track"],
        )
        if os.path.isfile(os.path.join(self.base_path, "track_metadata.csv")):
            df = pd.concat([
                pd.read_csv(os.path.join(self.base_path, "track_metadata.csv")),
                df
            ], axis=0)
        df.to_csv(os.path.join(self.base_path, "track_metadata.csv"), index=False)  
        
    
    async def get_(self, func, type_of_columns, dir):
        list_of_elements = await asyncio.to_thread(list, func(self.track_id))
        pd.DataFrame(
            [list(attrgetter(*get_config()[type_of_columns])(element)) for element in list_of_elements],
            columns=get_config()[type_of_columns],
        ).to_csv(os.path.join(self.base_path, dir, f"{self.track_id}.csv"), index=False)
        
        
    async def get_data(self, *string_functions):
        if string_functions == ():
            return await asyncio.gather(
                *[
                    self.get_(*self.map_of_func[i]) for i in self.map_of_func.keys()
                ]
            )
        return await asyncio.gather(
            *[
                self.get_(*self.map_of_func[i]) for i in string_functions
            ]
        )