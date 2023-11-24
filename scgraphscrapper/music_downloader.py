import pathlib
import os 
from soundcloud import SoundCloud
from scdl.scdl import (
    get_config,
    validate_url,
    download_url,
)
import sys 

arguments = {
    "--client-id": None,
    "--auth-token": None,
}
def download_musics(
    list_of_music_links: list[str], 
    list_of_music_ids:list[str], 
    path:str,
    force_redownload:bool = False, 
):
    arguments = {
        "--client-id": None,
        "--auth-token": None,
        "--path": path,
    }
    if "XDG_CONFIG_HOME" in os.environ:
        config_file = pathlib.Path(os.environ["XDG_CONFIG_HOME"], "scdl", "scdl.cfg")
    else:
        config_file = pathlib.Path.home().joinpath(".config", "scdl", "scdl.cfg")
            
    config = get_config(config_file)
    client_id = arguments["--client-id"] or config["scdl"]["client_id"]
    token = arguments["--auth-token"] or config["scdl"]["auth_token"]

    client = SoundCloud(client_id, token if token else None)

    path = arguments["--path"] or config["scdl"]["path"]
    if os.path.exists(path):
        os.chdir(path)
    else:
        sys.exit(1)


    for link, music_id in zip(list_of_music_links, list_of_music_ids):
        if os.path.isfile(music_id) and not force_redownload:
            continue
        
        arguments["--name-format"] = music_id
        arguments["-l"] = validate_url(client, link)
        python_args = {}
        for key, value in arguments.items():
            key = key.strip("-").replace("-", "_")
            python_args[key] = value
        download_url(client, **python_args)