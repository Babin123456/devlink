
import os
import re

replacements = {
    "frontend/src/features/dashboard/sections.tsx": [
        (
            "<<<<<<< ours\n  UserPlus,\n=======\n  TrendingUp,\n>>>>>>> theirs\n",
            "  UserPlus,\n  TrendingUp,\n"
        ),
        (
            "<<<<<<< ours\n  const { data = [] } = useQuery({\n    queryKey: [\"quick-actions\"],\n    queryFn: dashboardService.quickActions,\n  });\n\n  const getIcon = (name: string) => {\n    switch (name) {\n      case \"FolderPlus\":\n        return FolderPlus;\n      case \"Users2\":\n        return Users2;\n      case \"Flame\":\n        return Flame;\n      case \"UserPlus\":\n        return UserPlus;\n      default:\n        return FolderPlus;\n    }\n=======\n  const getIcon = (name: string) => {\n    switch (name) {\n      case \"FolderPlus\":\n        return FolderPlus;\n      case \"Users2\":\n        return Users2;\n      case \"Flame\":\n        return Flame;\n      case \"TrendingUp\":\n        return TrendingUp;\n      default:\n        return FolderPlus;\n    }\n>>>>>>> theirs\n",
            "  const { data = [] } = useQuery({\n    queryKey: [\"quick-actions\"],\n    queryFn: dashboardService.quickActions,\n  });\n\n  const getIcon = (name: string) => {\n    switch (name) {\n      case \"FolderPlus\":\n        return FolderPlus;\n      case \"Users2\":\n        return Users2;\n      case \"Flame\":\n        return Flame;\n      case \"UserPlus\":\n        return UserPlus;\n      case \"TrendingUp\":\n        return TrendingUp;\n      default:\n        return FolderPlus;\n    }\n"
        )
    ],
    "frontend/src/components/layout/TopNavbar.tsx": [
        (
            "<<<<<<< ours\n          <IconButton to=\"/messages\" count={3} ariaLabel=\"Messages\">\n=======\n          <IconButton to=\"/messages\" count={3} ariaLabel=\"Messages, 3 unread\">\n>>>>>>> theirs\n",
            "          <IconButton to=\"/messages\" count={3} ariaLabel=\"Messages, 3 unread\">\n"
        )
    ]
}

def process_file(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if filepath in replacements:
        for target, repl in replacements[filepath]:
            content = content.replace(target, repl)
    
    # For any remaining conflicts, we take theirs (group 2)
    def replacer(m):
        return m.group(2)
    
    # Non-greedy .*? to avoid eating everything between multiple conflicts
    content = re.sub(r"<<<<<<< ours\n(.*?)\n=======\n(.*?)\n>>>>>>> theirs\n", replacer, content, flags=re.DOTALL)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

for f in [
    "frontend/src/features/dashboard/sections.tsx",
    "frontend/src/components/layout/TopNavbar.tsx",
    "frontend/src/routes/_app.admin.jobs.tsx",
    "frontend/src/routes/_app.admin.search-analytics.tsx",
    "frontend/src/routes/_app.graph.tsx",
    "frontend/src/routes/_app.projects.tsx",
    "frontend/src/routes/_app.admin.maintenance.tsx",
    "frontend/src/routes/maintenance.tsx",
    "frontend/src/hooks/useProjectFilters.ts",
    "frontend/src/components/ui/filter-drawer.tsx"
]:
    process_file(f)

