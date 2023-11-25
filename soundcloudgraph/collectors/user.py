import typing as t
from utils import get_scrap_features
import asyncio
from operator import itemgetter
import pandas as pd 
import os 

features = get_scrap_features()

class CollectUser:
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
        self.client = client
        self.map_of_func = {
            "likes": [self.client.get_user_likes, "user", "likes"],
            "comments": [self.client.get_user_comments, "comment", "comments"],
            "followers": [self.client.get_user_followers, "user", "followers"],
            "following": [self.client.get_user_following, "user", "following"],
            "albums": [self.client.get_user_albums, "album", "albums"],
            "playlists": [self.client.get_user_playlists, "playlist", "playlists"],
            "related_artists": [self.client.get_user_related_artists, "user", "related_artists"],
            # "reposts": [self.client.get_user_reposts, ""],
            # "streams": [self.client.get_user_],
            "tracks": [self.client.get_user_tracks, "track", "tracks"],
        }
    
    async def get_(self, func, type_of_columns, dir):
        list_of_elements = await list(func(self.user_id))
        pd.DataFrame(
            [list(itemgetter(*features[type_of_columns]["list_columns"])(element.__dict__)) for element in list_of_elements],
            columns=features[type_of_columns]["list_columns"],
        ).to_csv(os.path.join(self.base_path, dir, f"{self.user_id}.csv"), index=False)

    
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