from mcp.server.fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("datetime_server")

@mcp.tool()
def get_current_datetime() -> str:
    """現在の日時を返す"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    mcp.run()
    
    
