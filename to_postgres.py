import os
from typing import List
from supabase import create_client, Client
from utils import URL, fetch_data, lightly_parse_data, SFAddress
from dotenv import load_dotenv


TABLE_NAME = "sf_addresses"


if __name__ == "__main__":
    load_dotenv()

    data = fetch_data(URL)
    address_data: List[SFAddress] = lightly_parse_data(data)

    # Connect to db
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)

    # Overwrite table with new data for simplicity
    supabase.table(TABLE_NAME).delete().neq("eas_fullid", "").execute()
    supabase.table(TABLE_NAME).insert([
        address.__dict__ for address in address_data
    ]).execute()