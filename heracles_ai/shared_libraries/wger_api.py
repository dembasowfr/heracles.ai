# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Shared utility functions for interacting with the WGER API."""

from typing import Dict, Any, Optional
import requests
import os

# Constants can also be defined here or imported from constants.py
WGER_API_BASE_URL = os.environ.get("HERACLES_WGER_API_BASE_URL")
WGER_API_KEY = os.environ.get("HERACLES_WGER_API_KEY")
ENGLISH_LANGUAGE_ID = os.environ.get("HERACLES_WGER_ENGLISH_LANGUAGE_ID")

def fetch_wger_data(endpoint_path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Fetches data from a specified WGER API endpoint.

    Args:
        api_key: The WGER API key for authentication.
        endpoint_path: The specific API endpoint path (e.g., '/exerciseinfo/', '/ingredient/').
        params: Optional dictionary of query parameters for the request.

    Returns:
        The parsed JSON response from the API.

    Raises:
        requests.exceptions.RequestException: If the API request fails.
        ValueError: If the response is not valid JSON.
    """
    if not WGER_API_KEY:
        raise ValueError("WGER API key is required.")

    headers = {
        'Authorization': f'Token {WGER_API_KEY}',
        'Accept': 'application/json'
    }
    params = {
        'language': ENGLISH_LANGUAGE_ID,
        'limit': 10,
    }
    
    url = f"{WGER_API_BASE_URL}{endpoint_path}"
    
    print(f"[WGER API Helper] Calling: {url} with params: {params}")

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[WGER API Helper] Request failed: {e}")
        raise # Re-raise the exception to be handled by the caller
    except requests.exceptions.JSONDecodeError as e:
        print(f"[WGER API Helper] Failed to decode JSON response: {e}")
        raise ValueError(f"Invalid JSON received from WGER API: {response.text}") from e
