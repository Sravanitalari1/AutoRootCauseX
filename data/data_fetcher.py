import requests
import pandas as pd

def fetch_complaints(make="TESLA", model="MODEL 3", year=2021, limit=100):
    base_url = "https://www.nhtsa.gov/webapi/api/Complaints/vehicle"
    params = {
        "make": make,
        "model": model,
        "modelYear": year,
        "format": "json"
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")

    data = response.json()
    complaints = data.get("Results", [])
    df = pd.DataFrame(complaints)
    
    if df.empty:
        return df

    return df[["ODINumber", "Component", "Summary", "FailureDate", "VehicleIdentificationNumber", "City", "State"]].head(limit)

if __name__ == "__main__":
    df = fetch_complaints()
    print(df.head())
