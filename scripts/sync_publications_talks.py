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

    if not os.path.exists(cv_path): return

    with open(cv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    talks_content = []
    current_video_html = "" 
    recording = False

    for line in lines:
        clean_line = line.strip()
        lower_line = clean_line.lower()

        if 'public talks' in lower_line and len(clean_line) < 40:
            recording = True
            continue
        if recording and len(clean_line) < 40:
            if any(x in lower_line for x in ['conference presentations', 'teaching', 'grants']):
                if current_video_html:
                    talks_content.append(current_video_html)
                    current_video_html = ""
                recording = False
                break

        if recording:
            stripped = line.lstrip()
            if not stripped.strip(): continue

            is_new_bullet = re.match(r'^(\*|-|\d+\.)\s', stripped)

            if is_new_bullet and current_video_html:
                talks_content.append(current_video_html)
                current_video_html = ""

            yt_match = re.search(r'(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+))', stripped)
            
            if yt_match:
                full_url = yt_match.group(1)
                video_id = yt_match.group(2)
                
                current_video_html = (
                    f'\n<div style="margin: 20px 0;">'
                    f'<a href="{full_url}" target="_blank">'
                    f'<img src="https://img.youtube.com/vi/{video_id}/maxresdefault.jpg" '
                    f'style="width:400px; border-radius:12px; box-shadow:0 6px 15px rgba(255,255,255,0.1); border: 1px solid #333;">'
                    f'</a></div>\n'
                )

            if is_new_bullet:
                talks_content.append(f"\n{stripped.strip()}")
            else:
                talks_content.append(f" {stripped.strip()}")

    if current_video_html:
        talks_content.append(current_video_html)

    if not talks_content: return

    if os.path.exists(talks_folder):
        shutil.rmtree(talks_folder)
    os.makedirs(talks_folder)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("---\ntitle: \"Talks\"\ncollection: talks\npermalink: /talks/\n---\n\n")
        f.write("".join(talks_content))

if __name__ == "__main__":
    sync_publications()
    sync_talks()
