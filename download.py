import requests
import json

API_KEY = "ArCskjn28L0gaCZI7hfASuYc3gCbhvoNAqOuphkT"  # Get one free at https://developer.nlr.gov/signup/

# Davidson County ZIP codes — union of Capitol Impact (authoritative government source)
# and Zillow, minus clearly out-of-county ZIPs (37027, 37024, 37086, 37143)
DAVIDSON_COUNTY_ZIPS = {
    # Suburban communities
    "37011",
    "37013",  # Antioch
    "37070",
    "37072",  # Goodlettsville
    "37076",  # Hermitage
    "37080",  # Joelton
    "37115",
    "37116",  # Madison
    "37138",  # Old Hickory
    "37189",  # Whites Creek
    # Nashville proper
    "37201",
    "37202",
    "37203",
    "37204",
    "37205",
    "37206",
    "37207",
    "37208",
    "37209",
    "37210",
    "37211",
    "37212",
    "37213",
    "37214",
    "37215",
    "37216",
    "37217",
    "37218",
    "37219",
    "37220",
    "37221",
    "37222",
    "37224",
    "37227",
    "37228",
    "37229",
    "37230",
    "37235",
    "37238",
    "37239",
    "37242",
    "37243",
    "37244",
    "37245",
    "37247",
    "37248",
    "37249",
    # Institutional / PO Box ZIPs within Nashville (hospitals, universities, gov)
    "37232",
    "37234",
    "37236",
    "37237",
    "37240",
    "37241",
    "37246",
    "37250",
}


def fetch_ev_stations_davidson() -> list[dict]:
    """Fetch all available EV charging stations in Davidson County, TN."""
    url = "https://developer.nlr.gov/api/alt-fuel-stations/v1.json"
    params = {
        "api_key": API_KEY,
        "fuel_type": "ELEC",
        "state": "TN",
        "status": "E",  # E = currently available; remove for planned/temp-unavailable too
        "limit": "all",
    }

    print("Fetching EV stations in Tennessee...")
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    all_stations = data["fuel_stations"]
    print(f"  Total TN stations fetched : {len(all_stations)}")

    davidson_stations = [
        s for s in all_stations if s.get("zip", "")[:5] in DAVIDSON_COUNTY_ZIPS
    ]
    print(f"  Davidson County stations  : {len(davidson_stations)}")
    return davidson_stations


def summarize(stations: list[dict]) -> None:
    """Print a human-readable summary of each station."""
    print("\n--- Stations ---")
    for s in stations:
        name = s.get("station_name", "N/A")
        address = s.get("street_address", "")
        city = s.get("city", "")
        zip_ = s.get("zip", "")
        network = s.get("ev_network") or "Non-Networked"
        l1 = s.get("ev_level1_evse_num") or 0
        l2 = s.get("ev_level2_evse_num") or 0
        dc = s.get("ev_dc_fast_num") or 0
        access = s.get("access_code", "")
        print(
            f"  [{access:7s}] {name} | {address}, {city} {zip_} | "
            f"Network: {network} | L1:{l1}  L2:{l2}  DC:{dc}"
        )


def print_stats(stations: list[dict]) -> None:
    """Print aggregate statistics."""
    total_l1 = sum(s.get("ev_level1_evse_num") or 0 for s in stations)
    total_l2 = sum(s.get("ev_level2_evse_num") or 0 for s in stations)
    total_dc = sum(s.get("ev_dc_fast_num") or 0 for s in stations)

    networks: dict[str, int] = {}
    for s in stations:
        net = s.get("ev_network") or "Non-Networked"
        networks[net] = networks.get(net, 0) + 1

    print("\n--- Aggregate Stats ---")
    print(f"  Total stations : {len(stations)}")
    print(f"  Level 1 ports  : {total_l1}")
    print(f"  Level 2 ports  : {total_l2}")
    print(f"  DC Fast ports  : {total_dc}")
    print(f"  Total ports    : {total_l1 + total_l2 + total_dc}")
    print("\n  By network:")
    for net, count in sorted(networks.items(), key=lambda x: -x[1]):
        print(f"    {net:30s} {count}")


if __name__ == "__main__":
    stations = fetch_ev_stations_davidson()

    # Save full JSON
    output_path = "davidson_ev_stations.json"
    with open(output_path, "w") as f:
        json.dump(stations, f, indent=2)
    print(f"\nSaved to {output_path}")

    print_stats(stations)
    summarize(stations)
