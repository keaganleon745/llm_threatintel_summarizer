# LLM-Powered Threat Intel Summarizer

## Why This Project
This project pulls in cybersecurity news from public sources like CISA, AlienVault, and the NVD, then uses a local or API-based language model (LLM) to summarize it all for you. The idea is to give analysts (or anyone interested) a quick, readable summary of what's happening in the current threat landscape.

---

## What It Does
- Grabs RSS feeds from popular threat intel sites
- Runs them through a summarizer (you can plug in your own LLM)
- Dumps everything into a simple text file
- Easy to expand with tools like LangChain or OpenAI

---

## Setup (Replit or Local)

1. Clone the Repo
```bash
git clone https://github.com/yourusername/llm-threatintel-summarizer.git
cd llm-threatintel-summarizer
```
2. Install Requirements
```bash
pip install -r requirements.txt
```
3. Run the Script
```bash
python llm_threatintel_summarizer.py
```
4. View Output

Check the summarized_threat_intel.txt file for the daily digest.
