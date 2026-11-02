"""Part 1's protocol server: no LLM or tools are implied by construction."""
import os
from mcp.server import MCPServer

HOST = "127.0.0.1"
PORT = int(os.getenv("MCP_PORT", "8080"))
mcp_server = MCPServer("MCP-RAG-app", instructions="Part 1 protocol foundation.")

if __name__ == "__main__":
    mcp_server.run(transport="streamable-http", host=HOST, port=PORT,
                   streamable_http_path="/mcp", json_response=True)
