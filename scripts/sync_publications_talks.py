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
    recording = False

    for line in lines:
        clean_line = line.strip()
        lower_line = clean_line.lower()

        if 'public talks' in lower_line and len(clean_line) < 40:
            recording = True
            continue
        if recording and len(clean_line) < 40:
            if any(x in lower_line for x in ['conference presentations', 'teaching', 'grants']):
                recording = False
                break

        if recording:
            stripped = line.lstrip()
            if not stripped.strip(): continue

            # Improved regex to catch the URL and video ID
            yt_match = re.search(r'(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+))', stripped)
            
            if yt_match:
                full_url = yt_match.group(1)
                video_id = yt_match.group(2)
                
                # 1. Prepare the video block
                yt_insert = (
                    f'\n<div style="margin: 15px 0;">'
                    f'<a href="{full_url}" target="_blank" style="text-decoration:none;">'
                    f'<img src="https://img.youtube.com/vi/{video_id}/mqdefault.jpg" style="width:240px; border-radius:8px; box-shadow:0 4px 10px rgba(0,0,0,0.15);">'
                    f'<div style="font-size:0.85em; color:black; font-weight:bold; margin-top:5px;">▶ Watch on YouTube</div>'
                    f'</a></div>\n'
                )
                
                # 2. Clean the line text
                # This regex looks for patterns like: (watch on Youtube [link]) or [watch on Youtube](link)
                # It handles the parentheses and the text within them.
                cleaned = stripped
                # Remove Markdown links: [watch on youtube](url) or similar
                cleaned = re.sub(r'\[[^\]]*watch on youtube[^\]]*\]\([^\)]*\)', '', cleaned, flags=re.IGNORECASE)
                # Remove plain text versions: (watch on youtube)
                cleaned = re.sub(r'\(\s*watch on youtube\s*\)', '', cleaned, flags=re.IGNORECASE)
                # Remove the URL if it's still hanging around
                cleaned = cleaned.replace(full_url, "")
                # Clean up any empty parentheses () or leftover "watch on youtube" strings
                cleaned = re.sub(r'watch on youtube', '', cleaned, flags=re.IGNORECASE)
                cleaned = re.sub(r'\(\s*\)', '', cleaned)
                
                # Final trim to remove trailing punctuation/spaces before the video insert
                cleaned = cleaned.strip().rstrip('.')
                
                # Append text first, then the video block
                talks_content.append(f"{cleaned}.\n{yt_insert}")
            else:
                # Handle standard list items or continuations
                if stripped[0].isdigit() and ". " in stripped[:4]:
                    talks_content.append(f"\n\n{stripped.strip()}")
                else:
                    talks_content.append(f" {stripped.strip()}")

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
