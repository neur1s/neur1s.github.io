import os
import shutil

def sync_publications():
    # Adjusted paths for AcademicPages structure
    cv_path = os.path.join('_pages', 'cv.md')
    pub_folder = '_publications'
    output_file = os.path.join(pub_folder, 'peer_reviewed_list.md')

    print(f"Looking for CV at: {cv_path}")
    if not os.path.exists(cv_path):
        # Fallback: check root if _pages fails
        if os.path.exists('cv.md'):
            cv_path = 'cv.md'
            print("Found cv.md in root instead of _pages.")
        else:
            print("CRITICAL ERROR: cv.md not found in root or _pages.")
            return

    with open(cv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    pub_content = []
    recording = False

    for line in lines:
        clean_line = line.strip().lower()
        
        # Start at Peer-reviewed header
        if 'peer-reviewed' in clean_line and '#' in line:
            recording = True
            continue
        
        # Stop at the next major section
        if recording and ('in preparation' in clean_line or 'talks' in clean_line or 'teaching' in clean_line) and '#' in line:
            recording = False
            break
        
        if recording:
            pub_content.append(line)

    if not pub_content:
        print("ERROR: Could not find 'Peer-reviewed' section text.")
        return

    # Ensure the _publications folder exists and is clean
    if os.path.exists(pub_folder):
        shutil.rmtree(pub_folder)
    os.makedirs(pub_folder)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("title: \"Peer-reviewed Publications\"\n")
        f.write("collection: publications\n")
        f.write("permalink: /publication/peer-reviewed\n")
        f.write("---\n\n")
        f.write('<div style="max-width: 1000px; margin: 0 auto;">\n\n')
        f.writelines(pub_content)
        f.write('\n</div>')

    print(f"SUCCESS: Created {output_file}")

if __name__ == "__main__":
    sync_publications()
