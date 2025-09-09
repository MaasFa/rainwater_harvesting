import requests
from datetime import datetime
def fetch_avg_annual_rainfall(lat: float, lon: float) -> float:
    """Fetch approximate avg annual rainfall (mm) using Open-Meteo monthly API as a best-effort.
    This function computes annual sum from monthly precipitation climatology if available.
    If external API fails, returns -1.0 to signal failure (caller may fallback to manual input).
    Note: network calls require outbound internet access at runtime.
    """
    try:
        # Open-Meteo Monthly Climate Averages (example endpoint)
        url = f"https://climate-api.open-meteo.com/v1/climate?latitude={lat}&longitude={lon}&monthly=precipitation_sum&start=1991-01&end=2020-12"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return -1.0
        data = resp.json()
        months = data.get('monthly', {}).get('precipitation_sum', [])
        if not months:
            return -1.0
        # months is a list of 12 monthly climatology values (mm/month); sum to annual
        annual = sum(months)
        return float(annual)
    except Exception:
        return -1.0
