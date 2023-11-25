import typing as t
from utils import get_scrap_features
import asyncio
from operator import itemgetter
import pandas as pd 
import os 

features = get_scrap_features()

class ScrapTrack:
    def __init__(
        self, 
        client, 
        user_id:str, 
        base_path:str, 
        permalink:t.Union[None, str] = None,
    ):
        if permalink:
            self.user_id = client.get_user_by_username(permalink).id
        else:
            self.user_id = user_id
        
        self.base_path = base_path
    
        self.map_of_func = {
            "albums": [self.client.get_track_albums, "album", "albums"],
            "playlists": [self.client.get_track_playlists, "playlist", "playlists"],
            "comments": [self.client.get_track_comments, "comment", "comments"],
            "likers": [self.get_track_likers, "user", "likers"],
            "reposters": [self.get_track_reposters, "user", "reposters"],
        }
    
    async def get_(self, func, type_of_columns, dir):
        list_of_elements = await list(func(self.user_id))
        pd.DataFrame(
            [list(itemgetter(*features[type_of_columns]["list_columns"])(element.__dict__)) for element in list_of_elements],
            columns=features[type_of_columns]["list_columns"],
        ).to_csv(os.path.join(self.base_path, dir, f"{self.user_id}.csv"), index=False)

    
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