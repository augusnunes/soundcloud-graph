import typing as t
from utils import get_scrap_features
import asyncio
from operator import itemgetter
import pandas as pd 
import os 

features = get_scrap_features()

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
    
    async def get_recent_tracks(self):
        list_of_recent_tracks = await list(self.client.get_tag_tracks_recent(self.tag))
        pd.DataFrame(
            [list(itemgetter(*features["track"]["list_columns"])(track.__dict__)) for track in list_of_recent_tracks],
            columns=features["track"]["list_columns"],
        ).to_csv(os.path.join(self.base_path, "recent_tracks", f"{self.user_id}.csv"), index=False)

    
    async def get_data(self):
        return await asyncio.gather(
            self.get_recent_tracks()
        )
        