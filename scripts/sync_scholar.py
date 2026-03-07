from scholarly import scholarly, ProxyGenerator
import yaml
import os

def sync_scholar():
    pg = ProxyGenerator()
    pg.FreeProxies() 
    scholarly.use_proxy(pg)
    scholar_id = '7ZBuO4wAAAAJ'
    
    print(f"Fetching data for scholar ID: {scholar_id}...")
    author = scholarly.search_author_id(scholar_id)
    scholarly.fill(author, sections=['publications'])
    
    publications = []
    for pub in author['publications']:
        p = {
            'title': pub['bib'].get('title', 'Unknown Title'),
            'year': pub['bib'].get('pub_year', 'N/A'),
            'citation': pub.get('num_citations', 0),
            # Extracting a cleaner URL if possible
            'url': f"https://scholar.google.com/citations?view_op=view_citation&citation_for_view={pub['author_pub_id']}"
        }
        publications.append(p)
    
    # Sort by year (newest first)
    publications.sort(key=lambda x: str(x['year']), reverse=True)

    # Ensure the _data directory exists (relative to the repo root)
    data_dir = os.path.join(os.path.dirname(__file__), '..', '_data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    output_path = os.path.join(data_dir, 'scholar_publications.yml')
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(publications, f, default_flow_style=False, sort_keys=False)
    
    print(f"Success! {len(publications)} publications saved to _data/scholar_publications.yml")

if __name__ == "__main__":
    sync_scholar()
