import typing as t
from .params import get_config
import asyncio
from operator import attrgetter
import pandas as pd 
import os 


class CollectTag:
    def __init__(
        self, 
        client, 
        tag:str, 
        base_path:str, 
    ):
        self.tag = tag
        self.client = client
        self.base_path = base_path
        
        if not os.path.exists(os.path.join(self.base_path,"recent_tracks")):
            os.makedirs(
                os.path.join(
                    self.base_path,
                    "recent_tracks"
                )
            )
        
    async def get_recent_tracks(self):
        
        list_of_recent_tracks = await asyncio.to_thread(list, self.client.get_tag_tracks_recent(self.tag))
        pd.DataFrame(
            [list(attrgetter(*get_config()["track"])(track)) for track in list_of_recent_tracks],
            columns=get_config()["track"],
        ).to_csv(os.path.join(self.base_path, "recent_tracks", f"{self.user_id}.csv"), index=False)

    
    async def get_data(self):
        return await asyncio.gather(
            self.get_recent_tracks()
        )
        