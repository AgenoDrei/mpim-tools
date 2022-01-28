import json
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

# print(names)
