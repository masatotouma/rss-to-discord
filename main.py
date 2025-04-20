import feedparser
import requests
import json
import os

# --- CONFIG ---
FEEDS = {
    "Twitter - @EPAKIM1": "https://nitter.privacydev.net/EPAKIM1/rss",
    "Twitter - @MasatoTouma": "https://nitter.privacydev.net/MasatoTouma/rss",
    "Twitter - @EPAKIM1": "https://nitter.poast.org/EPAKIM1/rss",
    "Twitter - @MasatoTouma": "https://nitter.poast.org/MasatoTouma/rss"
}

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")
SAVE_FILE = "last_seen.json"

# --- Load last seen post IDs ---
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        last_seen = json.load(f)
else:
    last_seen = {}

def send_to_discord(title, link, source):
    message = f"**New post from {source}**\n{title}\n{link}"
    requests.post(WEBHOOK_URL, json={"content": message})

# --- Process each feed ---
for source, url in FEEDS.items():
    feed = feedparser.parse(url)
    if not feed.entries:
        continue

    latest = feed.entries[0]
    entry_id = latest.get("id", latest.link)

    if last_seen.get(source) != entry_id:
        send_to_discord(latest.title, latest.link, source)
        last_seen[source] = entry_id

# --- Save updated post IDs ---
with open(SAVE_FILE, "w") as f:
    json.dump(last_seen, f)
