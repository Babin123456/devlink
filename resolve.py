
import os
import re

replacements = {
    "frontend/src/features/dashboard/sections.tsx": [
        (
            "<<<<<<< HEAD\n  UserPlus,\n=======\n  TrendingUp,\n>>>>>>> upstream/main\n",
            "  UserPlus,\n  TrendingUp,\n"
        ),
        (
            "<<<<<<< HEAD\n  const { data = [] } = useQuery({\n    queryKey: [\"quick-actions\"],\n    queryFn: dashboardService.quickActions,\n  });\n\n  const getIcon = (name: string) => {\n    switch (name) {\n      case \"FolderPlus\":\n        return FolderPlus;\n      case \"Users2\":\n        return Users2;\n      case \"Flame\":\n        return Flame;\n      case \"UserPlus\":\n        return UserPlus;\n      default:\n        return FolderPlus;\n    }\n=======\n  const getIcon = (name: string) => {\n    switch (name) {\n      case \"FolderPlus\":\n        return FolderPlus;\n      case \"Users2\":\n        return Users2;\n      case \"Flame\":\n        return Flame;\n      case \"TrendingUp\":\n        return TrendingUp;\n      default:\n        return FolderPlus;\n    }\n>>>>>>> upstream/main\n",
            "  const { data = [] } = useQuery({\n    queryKey: [\"quick-actions\"],\n    queryFn: dashboardService.quickActions,\n  });\n\n  const getIcon = (name: string) => {\n    switch (name) {\n      case \"FolderPlus\":\n        return FolderPlus;\n      case \"Users2\":\n        return Users2;\n      case \"Flame\":\n        return Flame;\n      case \"UserPlus\":\n        return UserPlus;\n      case \"TrendingUp\":\n        return TrendingUp;\n      default:\n        return FolderPlus;\n    }\n"
        )
    ]
}

# For the rest, we use upstream/main except graph.tsx
def process_file(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if filepath in replacements:
        for target, repl in replacements[filepath]:
            content = content.replace(target, repl)
    else:
        # Just take upstream/main
        def replacer(m):
            return m.group(2)
        content = re.sub(r"<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> upstream/main\n", replacer, content, flags=re.DOTALL)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

for f in [
    "frontend/src/features/dashboard/sections.tsx",
    "frontend/src/routes/_app.admin.jobs.tsx",
    "frontend/src/routes/_app.admin.search-analytics.tsx",
    "frontend/src/routes/_app.graph.tsx",
    "frontend/src/routes/_app.projects.tsx",
    "frontend/src/routes/_app.admin.maintenance.tsx",
    "frontend/src/hooks/useProjectFilters.ts",
    "frontend/src/components/ui/filter-drawer.tsx"
]:
    process_file(f)

