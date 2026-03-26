import feedparser
import requests
from pytrends.request import TrendReq
import random

def get_trending_topics(niche="facts trivia"):
    """Fetch trending topics using Google Trends + RSS feeds."""
    topics = []

    # Method 1: Google Trends
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([niche], timeframe='now 1-d', geo='')
        related = pytrends.related_queries()
        for key in related:
            if related[key]['top'] is not None:
                for row in related[key]['top'].itertuples():
                    topics.append(row.query)
    except Exception as e:
        print(f"[Trends] Error: {e}")

    # Method 2: Wikipedia "Did You Know" RSS feed
    try:
        wiki_feed = feedparser.parse(
            "https://en.wikipedia.org/w/index.php?title=Wikipedia:Recent_additions&action=raw"
        )
        # Use Wikipedia's random article API instead
        for _ in range(5):
            resp = requests.get(
                "https://en.wikipedia.org/api/rest_v1/page/random/summary",
                timeout=5
            )
            if resp.status_code == 200:
                data = resp.json()
                topics.append(data.get("title", "") + ": " + data.get("extract", "")[:200])
    except Exception as e:
        print(f"[Wiki] Error: {e}")

    # Method 3: Fallback evergreen topics
    fallback = [
        "mind-blowing science facts",
        "weird history facts nobody knows",
        "surprising animal facts",
        "psychology facts that change your behavior",
        "geography facts that sound impossible",
    ]
    topics.extend(fallback)

    # Return top 5 unique topics
    seen = set()
    unique = []
    for t in topics:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    return unique[:5]

if __name__ == "__main__":
    topics = get_trending_topics()
    for i, t in enumerate(topics, 1):
        print(f"{i}. {t}")