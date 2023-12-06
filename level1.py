from soundcloudgraph.scgraph import SoundCloudGraph

user_permalink = "bassmusicbrofc"
scg = SoundCloudGraph(f"data/level1/")

scg.collect_user(None, permalink=user_permalink)