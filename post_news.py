import tweepy
import feedparser
import json
import os

client = tweepy.Client(
    consumer_key=os.environ["TWITTER_KEY"],
    consumer_secret=os.environ["TWITTER_SECRET"],
    access_token=os.environ["TWITTER_TOKEN"],
    access_token_secret=os.environ["TWITTER_TOKEN_SECRET"]
)

POSTED_FILE = "posted.json"

if os.path.exists(POSTED_FILE):
    with open(POSTED_FILE) as f:
        posted = json.load(f)
else:
    posted = []

RSS_FEED = "https://feeds.bbci.co.uk/news/rss.xml"

feed = feedparser.parse(RSS_FEED)

for entry in feed.entries[:10]:
    if entry.link not in posted:
        tweet = f"{entry.title}\n\n{entry.link}"
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
        try:
            client.create_tweet(text=tweet)
            posted.append(entry.link)
            print(f"Posted: {entry.title}")
            break
        except Exception as e:
            print(f"Error: {e}")

with open(POSTED_FILE, "w") as f:
    json.dump(posted[-100:], f)
