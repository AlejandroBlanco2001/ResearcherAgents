import os
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

ARXIV_STORAGE_PATH = os.path.join(os.path.dirname(__file__), ".arxiv_storage")
os.makedirs(ARXIV_STORAGE_PATH, exist_ok=True)

# Create MCP toolsets as module-level instances to avoid conflicts in parallel execution
# These are created once and reused, preventing multiple MCP server process conflicts

mcp_arxiv = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uv",
            args=[
                "tool",
                "run",
                "arxiv-mcp-server",
                "--storage-path",
                os.path.abspath(ARXIV_STORAGE_PATH),
            ],
        ),
    ),
)

mcp_google_scholar = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uv",
            args=[
                "run",
                "-m",
                "paper_search_mcp.server",
            ],
        ),
    ),
)
