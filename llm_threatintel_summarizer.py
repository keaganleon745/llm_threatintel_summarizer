import feedparser
from datetime import datetime
import os
from dotenv import load_dotenv
from llama_cpp import Llama

load_dotenv()

# Path to your Mistral model (download it and place here)
MODEL_PATH = "models/mistral-7b-instruct.Q4_0.gguf"

# Load Mistral model
llm = Llama(model_path=MODEL_PATH, n_ctx=2048)

def summarize_with_local_llm(text):
    prompt = f"Summarize this in 2-3 sentences:\n\n{text.strip()}\n\nSummary:"
    result = llm(prompt, max_tokens=200, stop=["\n\n"])
    return result["choices"][0]["text"].strip()

def fetch_feed_items(feed_url):
    parsed_feed = feedparser.parse(feed_url)
    return parsed_feed.entries

def write_summary(feed_name, entries, f):
    for entry in entries:
        raw_text = entry.get('title', '') + "\n" + entry.get('summary', '')
        print(f"Summarizing entry from {feed_name}...")
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
