"""Entry point for the observability MCP server."""

import asyncio
import sys

from mcp_observability import main

if __name__ == "__main__":
    # Allow passing URLs as command-line arguments or use environment variables
    victorialogs_url = sys.argv[1] if len(sys.argv) > 1 else None
    victoriatrace_url = sys.argv[2] if len(sys.argv) > 2 else None
    asyncio.run(main(victorialogs_url, victoriatrace_url))
