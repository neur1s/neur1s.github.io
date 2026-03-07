import os

def sync_publications():
    cv_path = 'cv.md'
    pub_page_path = 'publications.md'

    if not os.path.exists(cv_path):
        print("cv.md not found.")
        return

    with open(cv_path, 'r') as f:
        lines = f.readlines()

    pub_content = []
    recording = False

    for line in lines:
        if 'Peer-reviewed' in line and '#' in line:
            recording = True
            # Add the header to the top of the list
            pub_content.append("## Peer-reviewed Publications\n\n")
            continue
        
        # Stop recording when we hit the next MAIN section header
        if recording and line.startswith('## '):
            recording = False
            break
        
        if recording:
            pub_content.append(line)

    if not pub_content:
        print("Could not find 'Peer-reviewed' section in cv.md")
        return


    with open(pub_page_path, 'w') as f:
        f.write("---\n")
        f.write("layout: page\n")
        f.write("title: Publications\n")
        f.write("permalink: /publications/\n")
        f.write("---\n\n")
        f.write('<div style="max-width: 1000px; margin: 0 auto;">\n\n')
        f.writelines(pub_content)
        f.write('\n</div>')

    print("Successfully synced Peer-reviewed publications!")

if __name__ == "__main__":
    sync_publications()
