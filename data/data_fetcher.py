# data/data_fetcher.py

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def fetch_complaints(make, model, year, limit=500):
    base_url = "https://www.nhtsa.gov/webapi/api/Complaints/vehicle"
    params = {
        "make": make,
        "model": model,
        "modelYear": year,
        "format": "json"
    }

    session = requests.Session()
    
    # Retry strategy for handling temporary failures
    retry = Retry(
        total=3,             # Retry up to 3 times
        backoff_factor=0.5,  # Wait 0.5s, 1s, then 2s
        status_forcelist=[500, 502, 503, 504],
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)

    try:
        response = session.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = data.get("Results", [])[:limit]
        return results
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch data from NHTSA: {e}")
        return []
