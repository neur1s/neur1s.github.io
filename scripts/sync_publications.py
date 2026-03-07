import os
import shutil

def sync_publications():
    cv_path = 'cv.md' 
    pub_folder = '_publications'
    output_file = os.path.join(pub_folder, 'peer_reviewed_list.md')

    if not os.path.exists(cv_path):
        print(f"ERROR: {cv_path} not found.")
        return

    with open(cv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    pub_content = []
    recording = False

    print("--- Scanning cv.md for Publications ---")
    for line in lines:
        clean_line = line.strip()
        lower_line = clean_line.lower()
        
        # START TRIGGER: Flexible detection
        # Matches "# Peer-reviewed", "**Peer-reviewed**", or "Peer-reviewed" (if short)
        if 'peer-reviewed' in lower_line and len(clean_line) < 40:
            print(f"DEBUG: START TRIGGER MATCHED -> {clean_line}")
            recording = True
            continue
        
        # STOP TRIGGER: When we hit the next section
        if recording and len(clean_line) < 40:
            if 'in preparation' in lower_line or 'talks' in lower_line or 'teaching' in lower_line:
                print(f"DEBUG: STOP TRIGGER MATCHED -> {clean_line}")
                recording = False
                break
        
        # CONTENT RECORDING with Spacing Logic
        if recording:
            if len(clean_line) > 0:
                pub_content.append(line)
            else:
                # Add an extra newline to ensure Markdown separates the papers
                pub_content.append("\n\n")

    if not pub_content:
        print("ERROR: Extraction failed. Markers not found.")
        # Debugging: show exactly what the script saw in the middle of the file
        midpoint = len(lines) // 2
        print(f"Sample lines from middle of file (lines {midpoint}-{midpoint+20}):")
        print("".join(lines[midpoint:midpoint+20]))
        return

    # Clean and Recreate folder
    if os.path.exists(pub_folder):
        shutil.rmtree(pub_folder)
    os.makedirs(pub_folder)

    # Write the collection file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("title: \"Peer-reviewed Publications\"\n")
        f.write("collection: publications\n")
        f.write("permalink: /publication/peer-reviewed\n")
        f.write("---\n\n")
        f.write('<div style="max-width: 1000px; margin: 0 auto;">\n\n')
        f.writelines(pub_content)
        f.write('\n</div>')
    
    print(f"SUCCESS: Created {output_file} with {len(pub_content)} lines.")

if __name__ == "__main__":
    sync_publications()
