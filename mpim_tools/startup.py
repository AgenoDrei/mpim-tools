import json

import pandas as pd
import toml
import os.path
from pathlib import Path

MAILGUN_BASE = "https://api.eu.mailgun.net/v3/"
HOME_DIR = Path.home()
CACHE_DIR = HOME_DIR / '.mpim_cache'
CONFIG_FILE = CACHE_DIR / 'config.json'
ROOT_PATH = Path(__file__).parent.parent
config = None
names = None
comp_matrix = None

if not os.path.exists(CACHE_DIR):
    os.mkdir(CACHE_DIR)

if os.path.exists(CONFIG_FILE):
    f = open(CONFIG_FILE)
    config = json.load(f)

if os.path.exists(os.path.join(ROOT_PATH, "names.toml")):
    names = toml.load(os.path.join(ROOT_PATH, "names.toml"))
elif os.path.exists("names.toml"):
    names = toml.load("names.toml")
elif os.path.exists(os.path.join( Path(__file__), "names.toml")):
    names = toml.load(os.path.join( Path(__file__), "names.toml"))
else:
    print(ROOT_PATH)
    raise FileNotFoundError("Could not find name definitions")

comp_path = "mtbi_table.cvs"
if os.path.exists(os.path.join(ROOT_PATH, comp_path)):
    comp_matrix = pd.read_csv(os.path.join(ROOT_PATH, comp_path), index_col=0)
elif os.path.exists(os.path.join( Path(__file__), comp_path)):
    comp_matrix = pd.read_csv(os.path.join( Path(__file__), comp_path), index_col=0)
else:
    raise FileNotFoundError("Could not find compatibility table")

# print(names)
