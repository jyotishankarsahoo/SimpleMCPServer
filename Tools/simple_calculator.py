from mcp.server.fastmcp import FastMCP
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("calculator-server")
mcp = FastMCP("Simple-Calculator")

@mcp.tool()
def add_numbers(a: int, b: int):
    "Add Two integers and returns result"
    return int(a) + int(b)

@mcp.tool()
def subtract_numbers(a: int, b: int):
    "Subtract Two integers and returns result"
    return int(a) - int(b)

@mcp.tool()
def multiply_numbers(a: int, b: int):
    "Multiply Two integers and returns result"
    return int(a) * int(b)

@mcp.tool()
def divide_numbers(a: int, b: int):
    "Divide Two integers and returns result"
    if b == 0:
        return "Error: Cannot divide by zero"
    return int(a) / int(b)

## npx @modelcontextprotocol/inspector python command to connect to MCP Inspector
if __name__ == "__main__":
    logger.info("Starting Simple-Calculator MCP Server...")
    mcp.run()