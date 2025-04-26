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

"""Fitness-related tools for Heracles.AI."""

from typing import Dict, Any
import google.adk.tools as ToolContext
import requests
import os
# --- Add import for the helper function ---
from heracles_ai.shared_libraries.wger_api import fetch_wger_data, WGER_API_KEY, ENGLISH_LANGUAGE_ID

def fitness_tool(query: str, tool_context: ToolContext) -> Dict[str, str]:
    """
    (Simulated) Gets meal and snack suggestions aligned with dietary needs and goals.

    Args:
        query: A description of the dietary needs (e.g., "vegetarian high-protein snacks").
        tool_context: The ADK tool context.

    Returns:
        A status message or simulated meal data.
    """
    # In a real implementation, this would query a nutrition database or API.
    print(f"[nutrition_tool called with query: {query}]")
    # Simulate finding some meal ideas
    simulated_meals = [
        {"meal_type": "snack", "name": "Greek Yogurt with Berries"},
        {"meal_type": "lunch", "name": "Lentil Soup with Whole Wheat Bread"},
        {"meal_type": "dinner", "name": "Tofu Stir-fry with Brown Rice"}
    ]
    # For now, just return a status message. The agent prompt expects this tool
    # to be used, but the agent itself will generate the plan text.
    # Alternatively, return the simulated data as a JSON string:
    # import json
    # return {"meals": json.dumps(simulated_meals)}
    return {"status": f"Simulated finding meal suggestions for: {query}"}
# # --- Updated Tool Function ---
# def fitness_tool(query: str, params, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Finds suitable exercises using the WGER API based on a query.
    Uses the fetch_wger_data helper function.
    Filters by English language and the provided query string.

    Args:
        query: A description of the exercises needed (e.g., "dumbbell exercises for chest").
        tool_context: The ADK tool context containing session state.

    Returns:
        A dictionary containing a list of exercises or an error/status message.
    """

    

    
    endpoint_path = "/exerciseinfo/"
    print(f"[fitness_tool] Calling WGER API via helper: {endpoint_path} with params: {params}")

    try:
        # --- Use the helper function ---
        data = fetch_wger_data(endpoint_path=endpoint_path, params=params)

        exercises = data.get('results', [])

        if not exercises:
            return {"status": f"No specific exercises found on WGER for query: '{query}' with filters {params}. Try a broader search."}

        formatted_exercises = [
            {
                "id": ex.get('id'),
                "name": ex.get('name'),
                "description": ex.get('description', '').replace('<p>', '').replace('</p>', ''),
                "category": ex.get('category', {}).get('name'),
                "equipment": [eq.get('name') for eq in ex.get('equipment', [])]
            }
            for ex in exercises
        ]

        print(f"[fitness_tool] Found {len(formatted_exercises)} exercises from WGER.")
        return {"exercises": formatted_exercises}

    # --- Catch exceptions raised by the helper ---
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"[fitness_tool] Error fetching or processing WGER data: {e}")
        return {"error": f"Failed to fetch exercises from WGER: {e}"}
    except Exception as e:
        print(f"[fitness_tool] An unexpected error occurred: {e}")
        return {"error": f"An unexpected error occurred while fetching exercises: {e}"}