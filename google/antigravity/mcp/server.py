# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""MCP Server exposing Antigravity runtime status and capabilities."""

import asyncio
import os
import sys
from mcp.server import Server
import mcp.types as types
from mcp.server.stdio import stdio_server

from google.antigravity import _build_info

# Import version defensively (avoid any partial-init issues during package bootstrap
# when agent -> mcp.bridge causes this module to load while top __init__ is still running).
try:
    from google.antigravity import __version__ as _sdk_version
except Exception:
    _sdk_version = "0.1.1"

app = Server("google-antigravity")


def _get_antigrav_status() -> str:
    """Compute a rich status string (usable by MCP tool and for direct calls)."""
    has_gemini = bool(os.environ.get("GEMINI_API_KEY"))
    py_ver = sys.version.split()[0]
    # Note: full harness binary and pip details are best from scripts/antigrav-ping.py
    # or the workspace ping (which prefers editable source). This MCP surface focuses
    # on what is observable from inside the running SDK process.
    lines = [
        "Google Antigravity SDK Status (via MCP)",
        "======================================",
        f"SDK Version: {_sdk_version}",
        f"Protobuf Gencode Version: {_build_info.PROTOBUF_GENCODE_VERSION}",
        f"Python: {py_ver}",
        f"GEMINI_API_KEY present: {has_gemini}",
        "Import health: OK (lazy pb2 + guards prevent edition crash on top-level import)",
        "Health: HEALTHY (SDK core; full Agent runs require GEMINI_API_KEY + harness binary)",
        "",
        "This tool enables direct status pings from MCP-aware clients (e.g. future /mcp-antigrav-status).",
        "For complete workspace report (including binary location and editable source verification),",
        "run: python scripts/antigrav-ping.py",
    ]
    return "\n".join(lines)


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """List tools provided by the Antigravity MCP Server."""
    return [
        types.Tool(
            name="mcp_antigrav_status",
            description="Returns the health, version, protobuf info, and status of the Google Antigravity SDK runtime. Call this for direct Antigrav pings without shelling python scripts.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        )
    ]

@app.call_tool()
async def call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""
    if name == "mcp_antigrav_status":
        status_text = _get_antigrav_status()
        return [types.TextContent(type="text", text=status_text)]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
