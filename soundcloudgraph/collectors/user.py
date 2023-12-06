import typing as t
import asyncio
from operator import attrgetter
import pandas as pd 
import os 
from .params import get_config
from soundcloud.resource.stream import PlaylistStreamRepostItem, PlaylistStreamItem, TrackStreamRepostItem, TrackStreamItem
from soundcloud.resource.like import PlaylistLike, TrackLike

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
            "likes": self.get_likes,
            "comments": [self.client.get_user_comments, "comment", "comments"],
            "followers": [self.client.get_user_followers, "user", "followers"],
            "following": [self.client.get_user_following, "user", "following"],
            "albums": [self.client.get_user_albums, "album", "albums"],
            "playlists": [self.client.get_user_playlists, "playlist", "playlists"],
            "related_artists": [self.client.get_user_related_artists, "user", "related_artists"],
            # "reposts": [self.client.get_user_reposts, "repost", "reposts"],
            "stream": self.get_stream,
            "tracks": [self.client.get_user_tracks, "track", "tracks"],
            "user_metadata": self.get_user_metadata
        }
        for i in self.map_of_func.keys():
            if not os.path.exists(os.path.join(self.base_path,i)) and i != "user_metadata":
                os.makedirs(
                    os.path.join(
                        self.base_path,
                        i
                    )
                )
    
    def get_stream_data(self, element):
        if isinstance(element, TrackStreamItem):
            data = [
                "track",
                False,
                element.track.id,
                element.track.user_id,
            ]
            
        elif isinstance(element, TrackStreamRepostItem):
            data = [
                "track",
                True,
                element.track.id,
                element.track.user_id,
            ]
            
        elif isinstance(element, PlaylistStreamItem):
            data = [
                "playlist",
                False,
                element.playlist.id,
                element.playlist.user_id,
            ]
            
        elif isinstance(element, PlaylistStreamRepostItem):
            data = [
                "playlist",
                True,
                element.playlist.id,
                element.playlist.user_id,
            ]
        data.append(element.created_at)
        return data
    
    # def get_repost_data(self, element):
        
    
    async def get_user_metadata(self):
        df = pd.DataFrame(
            [list(attrgetter(*get_config()["user"])(self.client.get_user(self.user_id)))],
            columns = get_config()["user"],
        )
        if os.path.isfile(os.path.join(self.base_path, "user_metadata.csv")):
            df = pd.concat([
                pd.read_csv(os.path.join(self.base_path, "user_metadata.csv")),
                df
            ], axis=0).drop_duplicates()
        df.to_csv(os.path.join(self.base_path, "user_metadata.csv"), index=False)  
    
    async def get_stream(self):
        if os.path.isfile(os.path.join(self.base_path, "stream", f"{self.user_id}.csv")) and not self.force_redownload:
            return
        try:
            list_of_stream = await asyncio.to_thread(list, self.client.get_user_stream(self.user_id)) 
        except:
            return 
        pd.DataFrame(
            [self.get_stream_data(stream) for stream in list_of_stream],
            columns=get_config()["stream"],
        ).to_csv(os.path.join(self.base_path, "stream", f"{self.user_id}.csv"), index=False)
    
    async def get_likes(self):
        if os.path.isfile(os.path.join(self.base_path, "likes", f"{self.user_id}.csv")) and not self.force_redownload:
            return 
        # while True:
        try:
            list_of_elements = await asyncio.to_thread(list, self.client.get_user_likes(self.user_id)) 
                # break 
        except:
            return
            # continue 
        pd.DataFrame(
            [list(attrgetter(*get_config()["tracklike"])(element))+["track"] if isinstance(element, TrackLike) else list(attrgetter(*get_config()["playlistlike"])(element))+["playlist"] for element in list_of_elements],
            columns=["created_at", "id", "user_id", "kind"],
        ).to_csv(os.path.join(self.base_path, "likes", f"{self.user_id}.csv"), index=False)

        
    
    async def get_(self, func, type_of_columns, dir):
        if os.path.isfile(os.path.join(self.base_path, dir, f"{self.user_id}.csv")) and not self.force_redownload:
            return 
        list_of_elements = [] 
        try: 
            for i in func(self.user_id):
                list_of_elements.append(i)
        except:
            pass
        pd.DataFrame(
            [list(attrgetter(*get_config()[type_of_columns])(element)) for element in list_of_elements],
            columns=get_config()[type_of_columns],
        ).to_csv(os.path.join(self.base_path, dir, f"{self.user_id}.csv"), index=False)


    
    async def get_data(self, *string_functions):
        if string_functions == ():
            return await asyncio.gather(
                *[
                    self.get_(*self.map_of_func[i]) if i not in ["stream", "user_metadata", "likes"] else self.map_of_func[i]() for i in self.map_of_func.keys()
                ]
            )
        return await asyncio.gather(
            *[
                self.get_(*self.map_of_func[i]) if i not in ["stream", "user_metadata", "likes"] else self.map_of_func[i]() for i in string_functions
            ]
        )