from llm_threatintel_summarizer import generate_threat_intel_summary

FEEDS = [
    'https://www.cisa.gov/news.xml',
    'https://thehackernews.com/feeds/posts/default'
]
OUTPUT_FILE = "summarized_threat_intel.txt"

def main():
    print("Running threat intel summarizer...")
    generate_threat_intel_summary(FEEDS, OUTPUT_FILE)
    print("Done.")

if __name__ == '__main__':
    main()
