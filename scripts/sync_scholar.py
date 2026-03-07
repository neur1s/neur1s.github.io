import feedparser # You'll need to add this to your workflow
import yaml
import os

def sync_scholar():
    # Your ID is 7ZBuO4wAAAAJ
    # The RSS feed URL for your citations:
    rss_url = "https://scholar.google.com/citations?view_op=export_metadata&hl=en&user=7ZBuO4wAAAAJ&output=rss"
    
    print(f"Fetching RSS feed from Google Scholar...")
    feed = feedparser.parse(rss_url)
    
    if not feed.entries:
        print("No entries found. Google might be blocking the RSS request.")
        return

    publications = []
    for entry in feed.entries:
        # RSS usually gives: Title, Link, and Summary (which contains Year/Authors)
        p = {
            'title': entry.title,
            'url': entry.link,
            # RSS summary is a bit messy, but it usually contains the year
            'year': entry.published[:4] if hasattr(entry, 'published') else "N/A",
            'description': entry.summary if hasattr(entry, 'summary') else ""
        }
        publications.append(p)
        print(f"Fetched: {p['title']}")

    data_dir = os.path.join(os.path.dirname(__file__), '..', '_data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    with open(os.path.join(data_dir, 'scholar_publications.yml'), 'w', encoding='utf-8') as f:
        yaml.dump(publications, f, default_flow_style=False, sort_keys=False)
    
    print(f"Success! Saved {len(publications)} entries.")

if __name__ == "__main__":
    sync_scholar()
