import os

tests_dir = r'c:\Users\drish\Desktop\devlink\devlink\backend\tests'

for root, dirs, files in os.walk(tests_dir):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            orig = content
            
            content = content.replace('client.get("/', 'client.get("/api/')
            content = content.replace("client.get('/", "client.get('/api/")
            
            content = content.replace('client.post("/', 'client.post("/api/')
            content = content.replace("client.post('/", "client.post('/api/")
            
            content = content.replace('client.put("/', 'client.put("/api/')
            content = content.replace("client.put('/", "client.put('/api/")
            
            content = content.replace('client.patch("/', 'client.patch("/api/')
            content = content.replace("client.patch('/", "client.patch('/api/")
            
            content = content.replace('client.delete("/', 'client.delete("/api/')
            content = content.replace("client.delete('/", "client.delete('/api/")
            
            content = content.replace('client.websocket_connect("/', 'client.websocket_connect("/api/')
            content = content.replace("client.websocket_connect('/", "client.websocket_connect('/api/")
            
            # Undo incorrect ones
            content = content.replace('("/api/api/', '("/api/')
            content = content.replace("('/api/api/", "('/api/")
            
            content = content.replace('("/api/health', '("/health')
            content = content.replace("('/api/health", "('/health")
            
            content = content.replace('("/api/docs', '("/docs')
            content = content.replace("('/api/docs", "('/docs")
            
            content = content.replace('("/api/openapi.json', '("/openapi.json')
            content = content.replace("('/api/openapi.json", "('/openapi.json")

            content = content.replace('("/api/"', '("/"')
            content = content.replace("('/api/'", "('/')")
            
            if content != orig:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {file}")
