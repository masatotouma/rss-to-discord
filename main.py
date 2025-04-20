import feedparser
import requests
import json
import os

# --- CONFIG ---
FEED_URL = "https://nitter.privacydev.net/EPAKIM1/rss"
SOURCE_NAME = "@EPAKIM1"                      
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")
SAVE_FILE = "last_seen.json"
# --------------

def send_to_discord(title, link):
    message = f"**New post from {SOURCE_NAME}**\n{title}\n{link}"
    requests.post(WEBHOOK_URL, json={"content": message})

# Load last seen post
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        last_seen = json.load(f)
else:
    last_seen = {}

feed = feedparser.parse(FEED_URL)
if not feed.entries:
    exit()

latest = feed.entries[0]
entry_id = latest.get("id", latest.link)

if last_seen.get(SOURCE_NAME) != entry_id:
    send_to_discord(latest.title, latest.link)
    last_seen[SOURCE_NAME] = entry_id

with open(SAVE_FILE, "w") as f:
    json.dump(last_seen, f)
