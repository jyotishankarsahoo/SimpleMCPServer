import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("file-reader-server")
base_path = Path(os.getenv("BASE_PATH", "/tmp"))
mcp = FastMCP("File-Reader")

@mcp.tool()
def list_files(directory: str):
    "List all files in the given directory."
    try:
        path = base_path / directory
        path = path.resolve()
        path = Path(directory)
        if not path.exists():
            logger.warning(f"Directory {directory} does not exist.")
        if not path.is_dir():
            logger.warning(f"Path {directory} is not a directory.")
        files = [f for f in path.iterdir() if f.is_file()]
        logger.info(f"Found {len(files)} files in the directory {directory}.")
        return {f.name: f.stat().st_size for f in files}
    except Exception as e:
        logger.error(f"Error reading directory {directory}: {e}.")

@mcp.tool()
def read_file(file_path: str):
    "Reads Contents of a File"
    try:
        path = (base_path / file_path).resolve()
        if not str(path).startswith(str(base_path)):
            logger.warning(f"Attempt to access file outside base path: {file_path}")
            return "Error: Access denied."
        if not path.exists():
            logger.warning(f"File {file_path} does not exits")
            return f"Error: File '{file_path}' not found."
        if not path.is_file():
            logger.warning(f"Path {file_path} is not a file")
        with open(path, "r") as file:
            content = file.read()
            logger.info(f"Read content from file {file_path}.")
            return content
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}.")
        return f"Error: {str(e)}"

## npx @modelcontextprotocol/inspector python command to connect to MCP Inspector

if __name__ == "__main__":
    mcp.run()