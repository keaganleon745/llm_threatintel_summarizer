import feedparser
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Optional LLM packages (uncomment if using APIs)
# import openai
# from langchain.llms import OpenAI

# Load API key from .env
load_dotenv()
OTX_API_KEY = os.getenv("OTX_API_KEY")

# Settings
FEEDS = [
    'https://www.cisa.gov/news.xml',
    'https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss-analyzed.xml'
]
OUTPUT_FILE = "summarized_threat_intel.txt"

# Sample summarizer stub for llama.cpp or other model integration
def summarize_with_local_llm(text):
    """
    Replace this with your LLM inference code (e.g., llama.cpp or GPT4All binding).
    For now, it returns a placeholder summary.
    """
    return f"[Summary Placeholder]\n{text[:300]}..."

# Fetch RSS feed items
def fetch_feed_items(feed_url):
    parsed_feed = feedparser.parse(feed_url)
    return parsed_feed.entries

# Fetch OTX pulses with authentication
def fetch_otx_pulses():
    headers = {
        "X-OTX-API-KEY": OTX_API_KEY,
        "Accept": "application/json"
    }
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        pulses = response.json().get("results", [])
        return [{
            'title': pulse.get('name', ''),
            'summary': pulse.get('description', '')
        } for pulse in pulses]
    else:
        print(f"Failed to fetch OTX: {response.status_code}")
        return []

# Write output to file
def write_summary(feed_name, entries, f):
    for entry in entries:
        raw_text = entry.get('title', '') + "\n" + entry.get('summary', '')
        summary = summarize_with_local_llm(raw_text)
        f.write(f"--- {feed_name} ---\n")
        f.write(summary + "\n\n")

# Main driver function
def main():
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"Threat Intel Summary for {datetime.now().strftime('%Y-%m-%d')}\n\n")

        # Fetch and summarize OTX
        otx_entries = fetch_otx_pulses()
        write_summary("AlienVault OTX", otx_entries[:5], f)  # Limit to 5 entries

        # Fetch and summarize other feeds
        for feed in FEEDS:
            try:
                feed_name = feed.split("/")[2]
                entries = fetch_feed_items(feed)
                write_summary(feed_name, entries[:5], f)
            except Exception as e:
                f.write(f"Error fetching {feed}: {str(e)}\n\n")

if __name__ == '__main__':
    main()
