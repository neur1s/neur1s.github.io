import os
import shutil

def sync_publications():
    cv_path = 'cv.md'
    # AcademicPages uses this specific folder for the Publications tab
    pub_folder = '_publications' 
    output_file = os.path.join(pub_folder, 'peer_reviewed_list.md')

    if not os.path.exists(cv_path):
        print("cv.md not found. Make sure Pandoc ran first.")
        return

    # 1. Read the freshly generated CV
    with open(cv_path, 'r') as f:
        lines = f.readlines()

    pub_content = []
    recording = False

    for line in lines:
        clean_line = line.strip().lower()
        # START at Peer-reviewed
        if 'peer-reviewed' in clean_line and '#' in line:
            recording = True
            continue
        # STOP at the next section (In Preparation, Talks, etc.)
        if recording and ('in preparation' in clean_line or 'talks' in clean_line) and '#' in line:
            recording = False
            break
        
        if recording:
            pub_content.append(line)

    if not pub_content:
        print("Extraction failed: Could not find 'Peer-reviewed' section.")
        return

    # 2. Clean the _publications folder so we don't have duplicates
    if os.path.exists(pub_folder):
        shutil.rmtree(pub_folder)
    os.makedirs(pub_folder)

    # 3. Create the "Collection" file that AcademicPages expects
    with open(output_file, 'w') as f:
        f.write("---\n")
        f.write("title: \"Peer-reviewed Publications\"\n")
        f.write("collection: publications\n")
        # This permalink tells the theme where to display this specific entry
        f.write("permalink: /publication/peer-reviewed\n")
        f.write("---\n\n")
        # Apply our 1000px width fix here too!
        f.write('<div style="max-width: 1000px; margin: 0 auto;">\n\n')
        f.writelines(pub_content)
        f.write('\n</div>')

    print(f"Success: Extracted {len(pub_content)} lines to {output_file}")

if __name__ == "__main__":
    sync_publications()
