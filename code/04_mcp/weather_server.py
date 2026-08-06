from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather_server")

@mcp.tool()
def get_weather(city: str) -> str:
    """指定した都市の天気を返す"""
    my_data = {
        "Tokyo": "晴れ、気温28度",
        "Osaka": "曇り、気温25度",
        "Sapporo": "雨、気温18度",
    }
    my_available = ", ".join(my_data.keys())
    return my_data.get(city,  f"'{city}' は未登録です。利用可能な都市: {my_available}")

if __name__ == "__main__":
    mcp.run()