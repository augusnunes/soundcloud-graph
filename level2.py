from soundcloudgraph.scgraph import SoundCloudGraph
import pandas as pd 

path = "data/level1/users/playlists/942648061.csv"
playlist_ids = list(pd.read_csv(path).id.astype(str))
scg = SoundCloudGraph(f"data/level2/")
for i in playlist_ids:
    print(i)
    scg.collect_playlist(i)