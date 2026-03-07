import os
import shutil

def sync_publications():
    # LOOK IN THE ROOT (matching your YAML output)
    cv_path = 'cv.md' 
    pub_folder = '_publications'
    output_file = os.path.join(pub_folder, 'peer_reviewed_list.md')

    if not os.path.exists(cv_path):
        print(f"ERROR: {cv_path} not found in root.")
        return

    with open(cv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    pub_content = []
    recording = False

    for line in lines:
        clean_line = line.strip().lower()
        if 'peer-reviewed' in clean_line and ('#' in line or '**' in line):
            recording = True
            continue
        if recording and ('in preparation' in clean_line or 'talks' in clean_line) and ('#' in line or '**' in line):
            recording = False
            break
        if recording:
            if len(line.strip()) > 0:
                pub_content.append(line)
            else:
                pub_content.append("\n") 

    if not pub_content:
        print("ERROR: Could not find Peer-reviewed section in cv.md.")
        return

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
    
    print(f"Successfully created {output_file}")

if __name__ == "__main__":
    sync_publications()
