import feedparser
from datetime import datetime

# Sample summarizer stub
def summarize_with_local_llm(text):
    return f"[Summary Placeholder]\n{text[:300]}..."

def fetch_feed_items(feed_url):
    parsed_feed = feedparser.parse(feed_url)
    return parsed_feed.entries

def write_summary(feed_name, entries, f):
    for entry in entries:
        raw_text = entry.get('title', '') + "\n" + entry.get('summary', '')
        summary = summarize_with_local_llm(raw_text)
        f.write(f"--- {feed_name} ---\n")
        f.write(summary + "\n\n")

def generate_threat_intel_summary(feeds, output_file):
    print("Opening output file...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Threat Intel Summary for {datetime.now().strftime('%Y-%m-%d')}\n\n")
        for feed in feeds:
            try:
                feed_name = feed.split("/")[2]
                print(f"Fetching: {feed_name}")
                entries = fetch_feed_items(feed)
                print(f"Found {len(entries)} entries")
                write_summary(feed_name, entries[:5], f)
            except Exception as e:
                print(f"Error fetching {feed}: {str(e)}")
                f.write(f"Error fetching {feed}: {str(e)}\n\n")
