
import os
import re

def process_file(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if "sections.tsx" in filepath:
        content = content.replace("<<<<<<< HEAD\n  UserPlus,\n=======\n  TrendingUp,\n>>>>>>> upstream/main", "  UserPlus,\n  TrendingUp,")
        content = content.replace("<<<<<<< HEAD\n  const { data = [] } = useQuery({\n    queryKey: [\"quick-actions\"],\n    queryFn: dashboardService.quickActions,\n  });\n\n  const getIcon = (name: string) => {\n    switch (name) {\n      case \"FolderPlus\":\n        return FolderPlus;\n      case \"Users2\":\n        return Users2;\n      case \"Flame\":\n        return Flame;\n      case \"UserPlus\":\n        return UserPlus;\n      default:\n        return FolderPlus;\n    }\n=======\n  const getIcon = (name: string) => {\n    switch (name) {\n      case \"FolderPlus\":\n        return FolderPlus;\n      case \"Users2\":\n        return Users2;\n      case \"Flame\":\n        return Flame;\n      case \"TrendingUp\":\n        return TrendingUp;\n      default:\n        return FolderPlus;\n    }\n>>>>>>> upstream/main", "  const { data = [] } = useQuery({\n    queryKey: [\"quick-actions\"],\n    queryFn: dashboardService.quickActions,\n  });\n\n  const getIcon = (name: string) => {\n    switch (name) {\n      case \"FolderPlus\":\n        return FolderPlus;\n      case \"Users2\":\n        return Users2;\n      case \"Flame\":\n        return Flame;\n      case \"UserPlus\":\n        return UserPlus;\n      case \"TrendingUp\":\n        return TrendingUp;\n      default:\n        return FolderPlus;\n    }\n")
        
        # For the third conflict, just take upstream/main
        content = re.sub(r"<<<<<<< HEAD\n.*?\n=======\n(.*?)\n>>>>>>> upstream/main", lambda m: m.group(1), content, flags=re.DOTALL)

    else:
        # Take upstream/main (theirs) for everything else
        content = re.sub(r"<<<<<<< HEAD\n.*?\n=======\n(.*?)\n>>>>>>> upstream/main", lambda m: m.group(1), content, flags=re.DOTALL)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

for f in [
    "frontend/src/features/dashboard/sections.tsx",
    "frontend/src/routes/_app.admin.maintenance.tsx",
    "frontend/src/routes/maintenance.tsx"
]:
    process_file(f)

