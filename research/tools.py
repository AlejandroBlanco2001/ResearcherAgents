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


def evaluate_research_quality(
    confidence_scores: list[int],
    threshold: int = 50,
) -> dict:
    """
    Evaluate if the research quality meets the threshold to stop iterating.
    
    Use this tool to decide whether to continue searching for more papers
    or proceed to the final summary.

    Args:
        confidence_scores: List of confidence scores (1-10) for each paper.
        threshold: Minimum total confidence required to stop. Default is 50.

    Returns:
        A dictionary with:
        - total_confidence: Sum of all confidence scores
        - num_papers: Number of papers evaluated
        - average_confidence: Average confidence per paper
        - meets_threshold: Whether the threshold is met
        - recommendation: "STOP" if quality is sufficient, "CONTINUE" if more research needed
        - suggested_action: What to do next
    """
    total_confidence = sum(confidence_scores)
    num_papers = len(confidence_scores)
    average_confidence = total_confidence / num_papers if num_papers > 0 else 0.0
    meets_threshold = total_confidence >= threshold

    if meets_threshold:
        recommendation = "STOP"
        suggested_action = "Quality threshold met. Proceed to final summary."
    elif num_papers == 0:
        recommendation = "CONTINUE"
        suggested_action = "No papers found. Try different keywords."
    elif average_confidence < 5:
        recommendation = "CONTINUE"
        suggested_action = "Paper quality is low. Search with more specific keywords."
    else:
        recommendation = "CONTINUE"
        suggested_action = "Need more high-quality papers. Broaden or refine search."

    return {
        "total_confidence": total_confidence,
        "num_papers": num_papers,
        "average_confidence": round(average_confidence, 2),
        "meets_threshold": meets_threshold,
        "threshold": threshold,
        "recommendation": recommendation,
        "suggested_action": suggested_action,
    }
