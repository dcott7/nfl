import asyncio
import aiohttp
import requests
import re
import time
import json
import logging
from typing import List, Dict, Any, Tuple, Union


def clean_url(url: str):
    return url.replace(" ","%20")


def append_query_params(base_url: str, **params) -> str:
    """Helper to append query parameters to a URL, accounting for existing parameters."""
    delimiter = '&' if '?' in base_url else '?'
    query_string = '&'.join(f"{key}={value}" for key, value in params.items())
    return f"{base_url}{delimiter}{query_string}"


def fetch_page(url: str, text=False, return_url=False, proxy: str = None) -> Union[Dict[str, Any], Tuple[Dict[str, Any], str]]:
    """
    Fetch a single page with an optional proxy.
    """
    start_time = time.time()
    proxies = {"http": proxy, "https": proxy} if proxy else None
    url = clean_url(url)

    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        elapsed_time = time.time() - start_time
        logging.info(f"Successfully fetched URL: {url} in {elapsed_time:.2f} seconds.")
        
        data = response.text if text else response.json()
        
        if return_url:
            return data, response.url
        else:
            return data
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            logging.warning(f"Resource not found (404) for URL: {url}. Skipping.")
        else:
            logging.error(f"HTTP error {e.response.status_code} for URL: {url}. Details: {e}")
        return {} if not return_url else ({}, url)
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching URL: {url}. Details: {e}")
        return {} if not return_url else ({}, url)


def fetch_all_refs(base_url: str, limit: int = None, proxy: str = None) -> List[str]:
    """Fetch all references sequentially using an optional proxy."""
    refs = []

    page_limit = {'limit': limit} if limit else {}
    first_page_url = append_query_params(base_url, page=1, **page_limit)
    first_page_data = fetch_page(first_page_url, proxy=proxy)

    refs.extend(re.sub(r'\?.*', '', item["$ref"]) for item in first_page_data.get("items", []))
    page_count = first_page_data.get("pageCount", 1)

    for page in range(2, page_count + 1):
        page_url = append_query_params(base_url, page=page, **page_limit)
        page_data = fetch_page(page_url, proxy=proxy)
        refs.extend(re.sub(r'\?.*', '', item["$ref"]) for item in page_data.get("items", []))

    return list(set(refs))


def fetch_all_items(base_url: str, limit: int = None) -> List[Dict]:
    """Fetch all items across all pages sequentially."""
    all_items = []
    seen_items = set()

    page_limit = {'limit': limit} if limit else {}
    first_page_url = append_query_params(base_url, page=1, **page_limit)
    first_page_data = fetch_page(first_page_url)

    for item in first_page_data.get("items", []):
        item_json = json.dumps(item, sort_keys=True)
        if item_json not in seen_items:
            all_items.append(item)
            seen_items.add(item_json)

    page_count = first_page_data.get("pageCount", 1)

    for page in range(2, page_count + 1):
        page_url = append_query_params(base_url, page=page, **page_limit)
        page_data = fetch_page(page_url)
        for item in page_data.get("items", []):
            item_json = json.dumps(item, sort_keys=True)
            if item_json not in seen_items:
                all_items.append(item)
                seen_items.add(item_json)

    return all_items


async def fetch_page_async(session: aiohttp.ClientSession, url: str, text=False, proxy: str = None) -> Dict[str, Any]:
    """
    Asynchronously fetch a single page with an optional proxy.
    """
    start_time = asyncio.get_event_loop().time()
    url = clean_url(url)

    try:
        async with session.get(url, proxy=proxy) as response:
            response.raise_for_status()
            elapsed_time = asyncio.get_event_loop().time() - start_time
            logging.info(f"Successfully fetched URL: {url} in {elapsed_time:.2f} seconds.")
            if text:
                return await response.text()
            else:
                return await response.json()
    except aiohttp.ClientResponseError as e:
        if e.status == 404:
            logging.warning(f"Resource not found (404) for URL: {url}. Skipping.")
        else:
            logging.error(f"HTTP error {e.status} for URL: {url}. Details: {e}")
        return {}
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching URL: {url}. Details: {e}")
        return {}


async def fetch_all_refs_async(base_url: str, limit: int = None, proxy: str = None) -> List[str]:
    """Asynchronously fetch all references using an optional proxy."""
    page_limit = {'limit': limit} if limit else {}

    async with aiohttp.ClientSession() as session:
        first_page_url = append_query_params(base_url, page=1, **page_limit)
        first_page_data = await fetch_page_async(session, first_page_url, proxy=proxy)
        refs = [
            re.sub(r'\?.*', '', item["$ref"]) for item in first_page_data.get("items", [])
        ]
        page_count = first_page_data.get("pageCount", 1)

        tasks = [
            fetch_page_async(session, append_query_params(base_url, page=page, **page_limit), proxy=proxy)
            for page in range(2, page_count + 1)
        ]
        results = await asyncio.gather(*tasks)

        for page_data in results:
            refs.extend(
                re.sub(r'\?.*', '', item["$ref"]) for item in page_data.get("items", [])
            )

        return list(set(refs))


async def fetch_all_items_async(base_url: str, limit=None) -> List[Dict]:
    """Asynchronously fetch all items across all pages."""
    page_limit = {'limit': limit} if limit else {}

    async with aiohttp.ClientSession() as session:
        all_items = []
        seen_items = set()

        first_page_url = append_query_params(base_url, page=1, **page_limit)
        first_page_data = await fetch_page_async(session, first_page_url)
        
        for item in first_page_data.get("items", []):
            item_json = json.dumps(item, sort_keys=True)
            if item_json not in seen_items:
                all_items.append(item)
                seen_items.add(item_json)

        page_count = first_page_data.get("pageCount", 1)

        tasks = [
            fetch_page_async(session, append_query_params(base_url, page=page, **page_limit))
            for page in range(2, page_count + 1)
        ]
        results = await asyncio.gather(*tasks)

        for page_data in results:
            for item in page_data.get("items", []):
                item_json = json.dumps(item, sort_keys=True)
                if item_json not in seen_items:
                    all_items.append(item)
                    seen_items.add(item_json)

        return all_items
