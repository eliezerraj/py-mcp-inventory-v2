from src.mcp_server.config.settings import settings

PROTECT_RESOURCE_METADATA = {
    "resource": settings.MCP_PROTECTED_RESOURCE + "/mcp",
    "authorization_servers": [
        settings.AUTHORIZATION_SERVER
    ],
    "scopes_supported": [
        "resource:order",
        "resource:time_series_order_items",
        "tool:post_order",
        "tool:post_checkout"
    ],
    "roles_supported": [
        "order-admin-role",
        "order-all-role",
        "order-resource-role",
        "order-tool-role"
    ],
    "bearer_methods_supported": [
        "header",
    ],
}