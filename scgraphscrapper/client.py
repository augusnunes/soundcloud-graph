
import os 
import pathlib

from soundcloud import SoundCloud
from scdl.scdl import get_config

arguments = {
    "--client-id": None,
    "--auth-token": None,
}


def get_client():
    if "XDG_CONFIG_HOME" in os.environ:
        config_file = pathlib.Path(os.environ["XDG_CONFIG_HOME"], "scdl", "scdl.cfg")
    else:
        config_file = pathlib.Path.home().joinpath(".config", "scdl", "scdl.cfg")
        
    config = get_config(config_file)
    client_id = arguments["--client-id"] or config["scdl"]["client_id"]
    token = arguments["--auth-token"] or config["scdl"]["auth_token"]

    return SoundCloud(client_id, token if token else None)