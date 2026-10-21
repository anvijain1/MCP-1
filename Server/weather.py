from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")
# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


# Helper function to make API requests
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the National Weather Service API."""

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                headers=headers,
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as exc:
            print(f"HTTP error occurred: {exc}")
            return None


# Helper function to format weather alerts
def format_alert(feature: dict[str, Any]) -> str:
    """Format an alert feature into readable text."""

    properties = feature.get("properties", {})

    return (
        f"Event: {properties.get('event', 'Unknown')}\n"
        f"Area: {properties.get('areaDesc', 'Unknown')}\n"
        f"Severity: {properties.get('severity', 'Unknown')}\n"
        f"Description: {properties.get('description', 'No description available')}\n"
        f"Instructions: {properties.get('instruction', 'No instructions provided')}"
    )


# MCP Tool 1: Get active weather alerts
@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get active weather alerts for a US state.

    Args:
        state: Two-letter US state code, for example CA or NY.
    """

    state = state.strip().upper()

    if len(state) != 2 or not state.isalpha():
        return "Please provide a valid two-letter US state code."

    url = f"{NWS_API_BASE}/alerts/active/area/{state}"

    data = await make_nws_request(url)

    if not data:
        return "Unable to retrieve weather alerts."

    features = data.get("features", [])

    if not features:
        return f"No active weather alerts found for {state}."

    alerts = [format_alert(feature) for feature in features]

    return "\n\n---\n\n".join(alerts)


# MCP Tool 2: Get weather forecast
@mcp.tool()
async def get_forecast(
    latitude: float,
    longitude: float,
) -> str:
    """Get a weather forecast for US geographic coordinates.

    Args:
        latitude: Latitude of the location.
        longitude: Longitude of the location.
    """

    if not -90 <= latitude <= 90:
        return "Latitude must be between -90 and 90."

    if not -180 <= longitude <= 180:
        return "Longitude must be between -180 and 180."

    # Get the forecast URL for these coordinates
    points_url = (
        f"{NWS_API_BASE}/points/{latitude},{longitude}"
    )

    points_data = await make_nws_request(points_url)

    if not points_data:
        return (
            "Unable to retrieve location data. "
            "The coordinates may not be supported by NWS."
        )

    properties = points_data.get("properties", {})
    forecast_url = properties.get("forecast")

    if not forecast_url:
        return "No forecast URL was provided for this location."

    # Retrieve the actual forecast
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to retrieve the weather forecast."

    periods = (
        forecast_data.get("properties", {}).get("periods", [])
    )

    if not periods:
        return "No forecast periods are currently available."

    # Format the first five forecast periods
    results = []

    for period in periods[:5]:
        results.append(
            f"{period.get('name', 'Unknown period')}\n"
            f"Temperature: {period.get('temperature', 'N/A')} "
            f"{period.get('temperatureUnit', '')}\n"
            f"Wind: {period.get('windSpeed', 'N/A')} "
            f"{period.get('windDirection', '')}\n"
            f"Forecast: {period.get('detailedForecast', 'N/A')}"
        )

    return "\n\n---\n\n".join(results)


# Start the MCP server
if __name__ == "__main__":
    mcp.run()