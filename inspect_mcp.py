from mcp.server.mcpserver import MCPServer
import inspect

mcp = MCPServer("test")
print("Instance attributes:")
for item in dir(mcp):
    print(item)
