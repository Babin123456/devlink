import os

def replace_in_file(filepath, old, new):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace(old, new)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

base = r"c:\Users\drish\Desktop\devlink\devlink\frontend\src\routes"

# _app.settings.tsx
settings_path = os.path.join(base, "_app.settings.tsx")
replace_in_file(settings_path, 'variant={true ? "default" : "outline"}', 'variant="default"')
replace_in_file(settings_path, 'variant={false ? "default" : "outline"}', 'variant="outline"')

# the rest
files = [
    "_app.admin.notifications.tsx",
    "_app.admin.search-analytics.tsx",
    "_app.graph.tsx",
    "_app.messages.$conversationId.tsx"
]

for file in files:
    filepath = os.path.join(base, file)
    replace_in_file(filepath, ": any", ": unknown")

print("Done")
