import os
import shutil

def sync_publications():
    cv_path = os.path.join('_pages', 'cv.md')
    pub_folder = '_publications'
    output_file = os.path.join(pub_folder, 'peer_reviewed_list.md')

    if not os.path.exists(cv_path):
        print(f"CRITICAL ERROR: {cv_path} not found.")
        return

    with open(cv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    pub_content = []
    recording = False

    print("--- Scanning cv.md for markers ---")
    for line in lines:
        clean_line = line.strip()
        
        # START TRIGGER: Look for 'Peer-reviewed' regardless of # or **
        # We use .lower() to be case-insensitive
        if 'peer-reviewed' in clean_line.lower() and len(clean_line) < 30:
            print(f"DEBUG: START TRIGGER MATCHED on line: {clean_line}")
            recording = True
            pub_content.append("## Peer-reviewed Publications\n\n")
            continue
        
        # STOP TRIGGER: Look for the next section
        if recording and ('in preparation' in clean_line.lower() or 'talks' in clean_line.lower()) and len(clean_line) < 30:
            print(f"DEBUG: STOP TRIGGER MATCHED on line: {clean_line}")
            recording = False
            break
        
        if recording:
            pub_content.append(line)

    if not pub_content:
        print("CRITICAL ERROR: No content captured.")
        print("Showing first 30 lines of cv.md to see what Pandoc did:")
        for i, l in enumerate(lines[:30]):
            print(f"Line {i}: {l.strip()}")
        return

    if os.path.exists(pub_folder):
        shutil.rmtree(pub_folder)
    os.makedirs(pub_folder)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("title: \"Peer-reviewed Publications\"\n")
        f.write("collection: publications\n")
        f.write("permalink: /publication/peer-reviewed\n")
        f.write("---")
        f.write("\n\n")
        f.write('<div style="max-width: 1000px; margin: 0 auto;">\n\n')
        f.writelines(pub_content)
        f.write('\n</div>')

    print(f"SUCCESS: Created {output_file} with {len(pub_content)} lines.")

if __name__ == "__main__":
    sync_publications()
