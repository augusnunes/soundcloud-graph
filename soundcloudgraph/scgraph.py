from .collectors.playlist import CollectPlaylist
from .collectors.tag import CollectTag
from .collectors.track import CollectTrack
from .collectors.user import CollectUser

from utils import get_client
import os 
import asyncio

class SoundCloudGraph:
    def __init__(self,  base_path):
        self.client = get_client() 
        self.base_path = base_path
    
    def collect_user(self, user_id, columns=[], permalink=None):
        user = CollectUser(
            self.client, 
            user_id, 
            os.path.join(self.base_path, "users"),
            permalink=permalink   
        )
        asyncio.run(user.get_data(*columns))

    
    def collect_users(self, user_ids, columns=[]):
        users = [
            CollectUser(
                self.client, 
                user_id, 
                os.path.join(self.base_path, "users") 
            ) for user_id in user_ids
        ]
        asyncio.run(
            asyncio.gather(
                *[user.get_data(*columns) for user in users]
            )
        )
        
        
    def collect_playlist(self, playlist_id, columns=[]):
        playlist = CollectPlaylist(
            self.client, 
            playlist_id,
            os.path.join(self.base_path, "playlist")
        )
        asyncio.run(playlist.get_data(*columns))
    
    def collect_playlists(self, playlist_ids, columns=[]):
        playlists = [
            CollectPlaylist(
                self.client, 
                playlist_id,
                os.path.join(self.base_path, "playlist")
            ) for playlist_id in playlist_ids
        ]
        asyncio.run(
            asyncio.gather(
                *[playlist.get_data(*columns) for playlist in playlists]
            )
        )
    
    def collect_tag(self, tag_query):
        tag = CollectTag(
            self.client,
            tag_query,
            os.path.join(self.base_path, "tag")
        )
        asyncio.run(tag.get_data())
    
    def collect_tags(self, tags_list):
        tags = [
            CollectTag(
                self.client,
                tag,
                os.path.join(self.base_path, "tag")
            ) for tag in tags_list
        ]
        asyncio.run(
            asyncio.gather(
                *[tag_c.get_data() for tag_c in tags]
            )
        )
    
    def collect_track(self, track_id, columns=[]):
        track_c = CollectTrack(
            self.client,
            track_id,
            os.path.join(self.base_path, "track")
        )
        asyncio.run(track_c.get_data(*columns))
        
    
    def collect_tracks(self, track_ids, columns=[]):
        tracks_c = [
            CollectTrack(
                self.client,
                track_id,
                os.path.join(self.base_path, "track")
            ) for track_id in track_ids
        ] 
        asyncio.run(
            asyncio.gather(
                *[track_c.get_data(*columns) for track_c in tracks_c]
            )
        )