import os
import shutil
import re

def sync_publications():
    cv_path = 'cv.md' 
    pub_folder = '_publications'
    output_file = os.path.join(pub_folder, 'peer_reviewed_list.md')

    if not os.path.exists(cv_path):
        return

    with open(cv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    pub_content = []
    recording = False

    for line in lines:
        clean_line = line.strip()
        lower_line = clean_line.lower()
        
        if 'peer-reviewed' in lower_line and len(clean_line) < 40:
            recording = True
            continue
        if recording and len(clean_line) < 40:
            if 'in preparation' in lower_line or 'talks' in lower_line:
                recording = False
                break
        
        if recording:
            stripped = line.lstrip()
            
            if stripped and stripped[0].isdigit() and ". " in stripped[:4]:
                parts = stripped.split(". ", 1)
                num = parts[0]
                content = parts[1] if len(parts) > 1 else ""
                
                pub_content.append(f"\n\n{num}. {content.rstrip()}")
            
            elif "Role:" in stripped or "Contribution:" in stripped:
                pub_content.append(f"\n{stripped.rstrip()}")
            
            elif stripped.strip():
                pub_content.append(f" {stripped.strip()}") 
            
            else:
                continue

    if not pub_content:
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
        f.writelines(pub_content)

def sync_talks():
    cv_path = 'cv.md'
    talks_folder = '_talks'
    output_file = os.path.join(talks_folder, 'talks_list.md')

    print(f"--- Debugging sync_talks ---")
    if not os.path.exists(cv_path): 
        print(f"DEBUG ERROR: {cv_path} not found.")
        return

    with open(cv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    talks_content = []
    recording = False

    for i, line in enumerate(lines):
        clean_line = line.strip()
        lower_line = clean_line.lower()

        # Debug specific lines that might be headers
        if '#' in clean_line or len(clean_line) < 45 and len(clean_line) > 3:
            # This will print small lines to the log so we can see what the headings look like
            pass 

        # START at "Public Talks"
        if 'public talks' in lower_line and len(clean_line) < 40:
            print(f"DEBUG: MATCHED START MARKER 'Public Talks' at line {i}: {clean_line}")
            recording = True
            continue
        
        # STOP at "Conference Presentations" or "Teaching"
        if recording and len(clean_line) < 40:
            if 'conference presentations' in lower_line or 'teaching' in lower_line:
                print(f"DEBUG: MATCHED STOP MARKER at line {i}: {clean_line}")
                recording = False
                break

        if recording:
            stripped = line.lstrip()
            if not stripped.strip(): continue

            yt_match = re.search(r'(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+))', stripped)
            
            if yt_match:
                full_url = yt_match.group(1)
                video_id = yt_match.group(2)
                yt_insert = (
                    f'\n<div style="margin: 10px 0;">'
                    f'<a href="{full_url}" target="_blank" style="text-decoration:none;">'
                    f'<img src="https://img.youtube.com/vi/{video_id}/mqdefault.jpg" style="width:200px; border-radius:8px; box-shadow:0 4px 8px rgba(0,0,0,0.1);">'
                    f'<div style="font-size:0.8em; color:#e62117; font-weight:bold;">▶ Watch on YouTube</div>'
                    f'</a></div>\n'
                )
                stripped = stripped.replace(full_url, "").strip()
                talks_content.append(f"\n{stripped}{yt_insert}")
            else:
                if stripped and stripped[0].isdigit() and ". " in stripped[:4]:
                    talks_content.append(f"\n\n{stripped}")
                else:
                    talks_content.append(f" {stripped}")

    if not talks_content:
        print("DEBUG ERROR: No talks content captured. Did not find start/stop markers or section was empty.")
        # If it failed, let's print a chunk of the CV to see what's there
        print("DEBUG: Showing lines 100-200 of cv.md for inspection:")
        print("".join(lines[100:200]))
        return

    if not os.path.exists(talks_folder): 
        print(f"DEBUG: Creating folder {talks_folder}")
        os.makedirs(talks_folder)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("---\ntitle: \"Talks\"\ncollection: talks\npermalink: /talks/\n---\n\n")
        f.writelines(talks_content)
    print(f"DEBUG: Successfully created {output_file}")

if __name__ == "__main__":
    sync_publications()
    sync_talks()
