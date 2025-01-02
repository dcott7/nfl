import requests
import re
import time
import json
from typing import List, Dict, Any

from models.logger import Logger

def fetch_page(url: str) -> Dict[str, Any]:
    """Fetch a single page and return its JSON data."""
    
    start_time = time.time()

    response = requests.get(url)
    response.raise_for_status()

    elapsed_time = time.time() - start_time

    Logger.info(f"Successfully fetched URL: {url} in {elapsed_time:.2f} seconds.")

    return response.json()

def fetch_all_refs(base_url: str) -> List[str]:
    """Fetch all references sequentially."""
    
    refs = []
    
    # Fetch the first page and extract the total page count
    first_page_data = fetch_page(f"{base_url}?page=1")
    refs.extend(re.sub(r'\?.*', '', item["$ref"]) for item in first_page_data.get("items", []))
    page_count = first_page_data["pageCount"]

    # Fetch the remaining pages
    for page in range(2, page_count + 1):
        page_data = fetch_page(f"{base_url}?page={page}")
        refs.extend(re.sub(r'\?.*', '', item["$ref"]) for item in page_data.get("items", []))

    return set(refs)

def fetch_all_items(base_url: str) -> List[Dict]:
    """Fetch all items across all pages sequentially."""
    
    all_items = []
    seen_items = set()
    
    first_page_data = fetch_page(f"{base_url}?page=1")
    for item in first_page_data.get("items", []):
        item_json = json.dumps(item, sort_keys=True)
        if item_json not in seen_items:
            all_items.append(item)
            seen_items.add(item_json)

    page_count = first_page_data["pageCount"]

    for page in range(2, page_count + 1):
        page_data = fetch_page(f"{base_url}?page={page}")
        for item in page_data.get("items", []):
            item_json = json.dumps(item, sort_keys=True)
            if item_json not in seen_items:
                all_items.append(item)
                seen_items.add(item_json)

    return all_items