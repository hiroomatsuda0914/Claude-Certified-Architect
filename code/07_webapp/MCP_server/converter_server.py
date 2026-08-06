# MCPサーバーの例

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("converter_server")


@mcp.tool()
def celsius_to_fahrenheit(celsius: float) -> str:
    """摂氏を華氏に変換する"""
    my_fahrenheit = celsius * 9 / 5 + 32
    return f"{celsius}°C = {my_fahrenheit}°F"

@mcp.tool()
def fahrenheit_to_celsius(fahrenheit: float) -> str:
    """華氏を摂氏に変換する"""
    my_celsius = (fahrenheit-32) * 5/9
    return f"{fahrenheit}°F = {my_celsius}°C"
    
if __name__ == "__main__":
    mcp.run()