from soundcloudgraph.scgraph import SoundCloudGraph
import pandas as pd 
import os 
from p_tqdm import p_map

path = "data/level2/playlist/tracks/"
l_dir = os.listdir(path)
df = pd.read_csv(path+l_dir[0])
i = 1
while i < len(l_dir):
    df = pd.concat([
        df,
        pd.read_csv(path+l_dir[i])
    ], axis=0)
    i += 1

list_of_user_id = df.user_id.drop_duplicates().astype(str).tolist()

scg = SoundCloudGraph(f"data/level3/")

p_map(scg.collect_user, list_of_user_id)

# for i in tqdm(list_of_user_id):
#     print(i)
#     scg.collect_user(str(i))