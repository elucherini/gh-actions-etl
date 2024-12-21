from dataclasses import dataclass
from typing import Any, Dict, List
import requests
import csv


URL = "https://data.sfgov.org/resource/ramy-di5m.geojson"


@dataclass
class SFAddress:
    """
    A dataclass to model a simple San Francisco address.
    """
    eas_baseid: str
    address: str
    zip: str
    latitude: float
    longitude: float


def fetch_data(url: str) -> Dict[str, Any]:
    """Fetch JSON data from our API endpoint.
    
    Args:
        url (str): The URL of the API endpoint.
    """
    try:
        # Send a GET request
        response = requests.get(url)
        
        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            return data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")


def lightly_parse_data(data: Dict[str, Any]) -> List[SFAddress]:
    """
    Lightly parse JSON data to extract only the relevant fields.

    Args:
        data (list): The JSON data to parse.
    """
    # Let's parse the JSON data to extract the relevant fields
    addresses: List[SFAddress] = []
    for feature in data["features"]:
        properties = feature["properties"]
        geometry = feature["geometry"]
        address = SFAddress(
            eas_baseid=properties.get("eas_baseid", ""),
            address=properties.get("address", ""),
            zip=properties.get("zip_code", ""),
            latitude=geometry["coordinates"][1],
            longitude=geometry["coordinates"][0]
        )
        addresses.append(address)

    return addresses


def save_to_csv(data: List[SFAddress], filename: str):
    """
    Save the data to a CSV file.

    Args:
        data (list): The data to save.
        filename (str): The name of the CSV file.
    """
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(SFAddress.__annotations__.keys())
        for address in data:
            writer.writerow(address.__dict__.values())


if __name__ == "__main__":
    data = fetch_data(URL)
    address_data = lightly_parse_data(data)
    save_to_csv(address_data, "output.csv")
