import requests
import logging
import sys
from mcp.server.fastmcp import FastMCP

# MCP サーバーでは stdout はプロトコル通信に使われるため stderr にログを出す
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

mcp = FastMCP("weather_server_v2")

def get_coordinates(city: str):
    """都市名から緯度・経度を取得"""
    logging.info(f"[Geocoding] '{city}' の座標を検索中...")
    my_res = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params = {"name": city, "count": 1, "language": "ja"}
    )
    my_data = my_res.json()
    if not my_data.get("results"):
        logging.warning(f"[Geocoding] '{city}' の座標が見つかりませんでした")
        return None
    my_result = my_data["results"][0]
    my_lat, my_lon = my_result["latitude"], my_result["longitude"]
    logging.info(f"[Geocoding] 取得成功: lat={my_lat}, lon={my_lon}")
    return my_lat, my_lon

@mcp.tool()
def get_weather(city: str) -> str:
    """指定した都市のリアルタイム天気を返す（Open-Meteo API使用）"""
    logging.info(f"[get_weather] 呼び出し: city='{city}'")

    my_coords = get_coordinates(city)
    if not my_coords:
        return f"都市名「{city}」の座標が見つかりませんでした。"

    my_lat, my_lon = my_coords
    logging.info(f"[Weather API] 気象データを取得中: lat={my_lat}, lon={my_lon}")
    my_res = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params = {
            "latitude": my_lat,
            "longitude": my_lon,
            "current": "temperature_2m,weathercode,windspeed_10m"
        }
    )
    my_current = my_res.json()["current"]
    my_temp = my_current["temperature_2m"]
    my_wind = my_current["windspeed_10m"]
    my_weather_code = my_current["weathercode"]

    my_result = f"{city}の現在の天気は、気温{my_temp}℃、風速{my_wind}m/s、天気コード{my_weather_code}です。"
    logging.info(f"[get_weather] 完了: {my_result}")
    return my_result

if __name__ == "__main__":
    mcp.run()