import mcp.server.mcpserver as m
import inspect

print("MCPServer attributes:")
for name, obj in inspect.getmembers(m.MCPServer):
    if not name.startswith("_"):
        print(f"  {name}: {type(obj)}")
