import typing as t
import asyncio
from operator import attrgetter
import pandas as pd 
import os 
from .params import get_config


class CollectUser:
    def __init__(
        self, 
        client, 
        user_id:str, 
        base_path:str, 
        permalink:t.Union[None, str] = None,
        force_redownload=False,
    ):
        if permalink:
            self.user_id = client.get_user_by_username(permalink).id
        else:
            self.user_id = user_id
        self.force_redownload = force_redownload
        self.base_path = base_path
        self.client = client
        self.map_of_func = {
            "likes": [self.client.get_user_likes, "like", "likes"],
            "comments": [self.client.get_user_comments, "comment", "comments"],
            "followers": [self.client.get_user_followers, "user", "followers"],
            "following": [self.client.get_user_following, "user", "following"],
            "albums": [self.client.get_user_albums, "album", "albums"],
            "playlists": [self.client.get_user_playlists, "playlist", "playlists"],
            "related_artists": [self.client.get_user_related_artists, "user", "related_artists"],
            "reposts": [self.client.get_user_reposts, "repost", "reposts"],
            # "streams": [self.client.get_user_],
            "tracks": [self.client.get_user_tracks, "track", "tracks"],
        }
        for i in self.map_of_func.keys():
            if not os.path.exists(os.path.join(self.base_path,i)):
                os.makedirs(
                    os.path.join(
                        self.base_path,
                        i
                    )
                )
    
    async def get_(self, func, type_of_columns, dir):
        if os.path.isfile(os.path.join(self.base_path, dir, f"{self.user_id}.csv")) and not self.force_redownload:
            return 
        list_of_elements = await asyncio.to_thread(list, func(self.user_id)) 
        print(f"Getting {dir}")
        pd.DataFrame(
            [list(attrgetter(*get_config()[type_of_columns])(element)) for element in list_of_elements],
            columns=get_config()[type_of_columns],
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