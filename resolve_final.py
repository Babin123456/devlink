
import os
import re

def process_file(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # For sections.tsx, keep both PR (ours) and upstream (theirs) for the first conflict
    if "sections.tsx" in filepath:
        content = content.replace("<<<<<<< ours\n  UserPlus,\n=======\n  TrendingUp,\n>>>>>>> theirs\n", "  UserPlus,\n  TrendingUp,\n")
        
        # The other conflicts in sections.tsx: keep ours for the second, theirs for the third, but we can also just use regex
        # Actually, let us just use ours for everything inside sections.tsx except the first conflict which we combined.
        def replacer_sections(m):
            return m.group(1) # ours
        content = re.sub(r"<<<<<<< ours\n(.*?)\n=======\n(.*?)\n>>>>>>> theirs\n", replacer_sections, content, flags=re.DOTALL)
    
    # For others, keep theirs
    else:
        def replacer(m):
            return m.group(2) # theirs
        content = re.sub(r"<<<<<<< ours\n(.*?)\n=======\n(.*?)\n>>>>>>> theirs\n", replacer, content, flags=re.DOTALL)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

for f in [
    "frontend/src/features/dashboard/sections.tsx",
    "frontend/src/routes/_app.admin.maintenance.tsx",
    "frontend/src/routes/maintenance.tsx"
]:
    process_file(f)

