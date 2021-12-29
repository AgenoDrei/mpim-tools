import json
import os.path
from pathlib import Path

MAILGUN_BASE = "https://api.eu.mailgun.net/v3/"
HOME_DIR = Path.home()
CACHE_DIR = HOME_DIR / '.mpim_cache'
CONFIG_FILE = CACHE_DIR / 'config.json'
config = None

if not os.path.exists(CACHE_DIR):
    os.mkdir(CACHE_DIR)

if os.path.exists(CONFIG_FILE):
    f = open(CONFIG_FILE)
    config = json.load(f)