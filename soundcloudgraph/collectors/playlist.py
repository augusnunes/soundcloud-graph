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
        force_redownload=False,
    ):
        self.playlist_id = playlist_id
        self.base_path = base_path
        self.client = client
        self.force_redownload = force_redownload
        self.map_of_func = {
            "likers": [self.client.get_playlist_likers, "user", "likers"],
            "reposters": [self.client.get_playlist_reposters, "user", "reposters"],
            "tracks": self.get_tracks,
            "playlist_metadata": self.get_playlist_metadata,
        }
        for i in self.map_of_func.keys():
            if not os.path.exists(os.path.join(self.base_path,i)) and i != "playlist_metadata":
                os.makedirs(
                    os.path.join(
                        self.base_path,
                        i
                    )
                )


    async def get_tracks(self):
        if os.path.isfile(os.path.join(self.base_path, "tracks", f"{self.playlist_id}.csv")) and not self.force_redownload:
            return 
        list_of_tracks = [
            self.client.get_track(str(track.id)) for track in  self.client.get_playlist(self.playlist_id).tracks
        ]
        pd.DataFrame(
            [list(attrgetter(*get_config()["track"])(element)) for element in list_of_tracks],
            columns=get_config()["track"],
        ).to_csv(os.path.join(self.base_path, "tracks", f"{self.playlist_id}.csv"), index=False)
    
    async def get_playlist_metadata(self):
        df = pd.DataFrame(
            [list(attrgetter(*get_config()["playlist"])(self.client.get_playlist(self.playlist_id)))],
            columns = get_config()["playlist"],
        )
        if os.path.isfile(os.path.join(self.base_path, "playlist_metadata.csv")):
            df = pd.concat([
                pd.read_csv(os.path.join(self.base_path, "playlist_metadata.csv")),
                df
            ], axis=0)
        df.to_csv(os.path.join(self.base_path, "playlist_metadata.csv"), index=False)        

        
    async def get_(self, func, type_of_columns, dir):
        if os.path.isfile(os.path.join(self.base_path, dir, f"{self.playlist_id}.csv")) and not self.force_redownload:
            return 
        list_of_elements = await asyncio.to_thread(list, func(self.playlist_id))
        pd.DataFrame(
            [list(attrgetter(*get_config()[type_of_columns])(element)) for element in list_of_elements],
            columns=get_config()[type_of_columns],
        ).to_csv(os.path.join(self.base_path, dir, f"{self.playlist_id}.csv"), index=False)
    
    async def get_data(self, *string_functions):
        if string_functions == ():
            return await asyncio.gather(
                *[
                    self.get_(*self.map_of_func[i]) if i not in ["tracks", "playlist_metadata"] else self.map_of_func[i]() for i in self.map_of_func.keys() 
                ]
            ) 
        return await asyncio.gather(
            *[
                self.get_(*self.map_of_func[i]) if i not in ["tracks", "playlist_metadata"] else self.map_of_func[i]() for i in string_functions
            ]
        )