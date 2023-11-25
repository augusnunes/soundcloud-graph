import typing as t
from utils import get_scrap_features
import asyncio
from operator import itemgetter
import pandas as pd 
import os 

features = get_scrap_features()

class User:
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
            "likes": [True, self.client.get_user_likes, "user", "likes"],
            "comments": [True, self.client.get_user_comments, "comment", "comments"],
            "followers": [True, self.client.get_user_followers, "user", "followers"],
            "following": [True, self.client.get_user_following, "user", "following"],
            "albums": [True, self.client.get_user_albums, "album", "albums"],
            "playlists": [True, self.client.get_user_playlists, "playlist", "playlists"],
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
    
    async def get_likes(self):
        list_of_likes = await list(self.client.get_user_likes(self.user_id))
        pd.DataFrame(
            [list(itemgetter(*features["track"]["list_columns"])(like.__dict__)) for like in list_of_likes],
            columns=features["track"]["list_columns"],
        ).to_csv(os.path.join(self.base_path, "likes", f"{self.user_id}.csv"), index=False)

    async def get_comments(self):
        list_of_comments = await list(self.client.get_user_comments(self.user_id))
        pd.DataFrame(
            [list(itemgetter(*features["comment"]["list_columns"])(comment.__dict__)) for comment in list_of_comments],
            columns=features["comment"]["list_columns"],
        ).to_csv(os.path.join(self.base_path, "comments", f"{self.user_id}.csv"), index=False)
              
    async def get_followers(self):
        list_of_followers = await list(self.client.get_user_followers(self.user_id))
        pd.DataFrame(
            [list(itemgetter(*features["user"]["list_columns"])(follower.__dict__)) for follower in list_of_followers],
            columns=features["user"]["list_columns"],
        ).to_csv(os.path.join(self.base_path, "followers", f"{self.user_id}.csv"), index=False)
           
    async def get_following(self):
        list_of_following = await list(self.client.get_user_following(self.user_id))
        pd.DataFrame(
            [list(itemgetter(*features["user"]["list_columns"])(following.__dict__)) for following in list_of_following],
            columns=features["user"]["list_columns"],
        ).to_csv(os.path.join(self.base_path, "following", f"{self.user_id}.csv"), index=False)
        
    async def get_albums(self):
        list_of_albums = await list(self.client.get_user_albums(self.user_id))
        pd.DataFrame(
            [list(itemgetter(*features["album"]["list_columns"])(album.__dict__)) for album in list_of_albums],
            columns=features["album"]["list_columns"],
        ).to_csv(os.path.join(self.base_path, "albums", f"{self.user_id}.csv"), index=False)
        
    async def get_playlists(self):
        list_of_playlists = await list(self.client.get_user_playlists(self.user_id))
        pd.DataFrame(
            [list(itemgetter(*features["playlist"]["list_columns"])(playlist.__dict__)) for playlist in list_of_playlists],
            columns=features["playlist"]["list_columns"],
        ).to_csv(os.path.join(self.base_path, "playlists", f"{self.user_id}.csv"), index=False)
    
    async def get_related_artists(self):
        list_of_related_artists = await list(self.client.get_user_related_artists(self.user_id))
        pd.DataFrame(
            [list(itemgetter(*features["user"]["list_columns"])(related_artists.__dict__)) for related_artists in list_of_related_artists],
            columns=features["user"]["list_columns"],
        ).to_csv(os.path.join(self.base_path, "related_artists", f"{self.user_id}.csv"), index=False) 
    
    async def get_reposts(self):
        list_of_reposts = await list(self.client.get_user_reposts(self.user_id))
        pd.DataFrame(
            [list(itemgetter(*features["album"]["list_columns"])(repost.__dict__)) for repost in list_of_reposts],
            columns=features["album"]["list_columns"],
        ).to_csv(os.path.join(self.base_path, "reposts", f"{self.user_id}.csv"), index=False) 
    
    async def get_streams(self):
        list_of_albums = await list(self.client.get_user_albums(self.user_id))
        pd.DataFrame(
            [list(itemgetter(*features["album"]["list_columns"])(album.__dict__)) for album in list_of_albums],
            columns=features["album"]["list_columns"],
        ).to_csv(os.path.join(self.base_path, "albums", f"{self.user_id}.csv"), index=False) 
    
    async def get_tracks(self):
        list_of_albums = await list(self.client.get_user_albums(self.user_id))
        pd.DataFrame(
            [list(itemgetter(*features["album"]["list_columns"])(album.__dict__)) for album in list_of_albums],
            columns=features["album"]["list_columns"],
        ).to_csv(os.path.join(self.base_path, "albums", f"{self.user_id}.csv"), index=False) 
    
    async def get_data(self, *functions, all_data:bool=False):
        if all_data:
            return await asyncio.gather(
                self.get_followers(),
                self.get_following(),
                self.get_albums(),
                self.get_playlists(),
                self.get_related_artists(),
                self.get_reposts(),
                self.get_streams(),
                self.get_tracks(),
            )
            
        return await asyncio.gather(
            *functions
        )