import os
import shutil

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

if __name__ == "__main__":
    sync_publications()
