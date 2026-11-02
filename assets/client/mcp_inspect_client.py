import argparse
import asyncio
import json
import os

import httpx
from mcp import ClientSession, types
from mcp.client.streamable_http import streamable_http_client

SERVER_MCP = "http://localhost:7500/mcp"

async def inspect_server(url: str) -> dict:
    token = os.environ.get("MCP_ACCESS_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    async with httpx.AsyncClient(headers=headers) as client:
        async with streamable_http_client(url, http_client=client) as (read, write):
            async with ClientSession(read, write) as session:
                initialized = await session.initialize()
                capabilities = initialized.capabilities
                report = {
                    "server": initialized.server_info.model_dump(
                        mode="json", by_alias=True, exclude_none=True
                    ),
                }

                for name, attribute, capability, list_items in (
                    ("tools", "tools", capabilities.tools, session.list_tools),
                    ("resources", "resources", capabilities.resources, session.list_resources),
                    (
                        "resourceTemplates",
                        "resource_templates",
                        capabilities.resources,
                        session.list_resource_templates,
                    ),
                    ("prompts", "prompts", capabilities.prompts, session.list_prompts),
                ):
                    if capability is None:
                        report[name] = None
                        continue

                    items = []
                    cursor = None
                    while True:
                        page = await list_items(
                            params=types.PaginatedRequestParams(cursor=cursor)
                            if cursor is not None
                            else None
                        )
                        items.extend(
                            item.model_dump(
                                mode="json", by_alias=True, exclude_none=True
                            )
                            for item in getattr(page, attribute)
                        )
                        cursor = page.next_cursor
                        if not cursor:
                            break
                    report[name] = items

                return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--url", default=SERVER_MCP, help=f"MCP endpoint (default: {SERVER_MCP})"
    )
    args = parser.parse_args()
    print(json.dumps(asyncio.run(inspect_server(args.url)), indent=2))


if __name__ == "__main__":
    main()