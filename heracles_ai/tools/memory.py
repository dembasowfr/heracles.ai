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

"""The 'memorize' tool for agents to manage session state (user profile, etc.)."""

from datetime import datetime
import json
import os
from typing import Any, Dict, Optional  # Import Optional

import google.adk as adk
from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.adk.tools import ToolContext

from heracles_ai.shared_libraries import constants  # Import constants from shared_libraries

# Assuming constants will be defined in shared_libraries
# from heracles_ai.shared_libraries import constants

# Define the path for loading initial user profile scenarios
SAMPLE_SCENARIO_PATH = os.getenv(
    "HERACLES_AI_SCENARIO", "eval/program_empty_default.json"
)


# Define the memorize_list tool function
def memorize_list(key: str, value: str, tool_context: ToolContext) -> Dict[str, str]:  # Changed value type to str
    """
    Memorizes a piece of information by appending it to a list associated with a key.
    Assumes the value provided is a string representation of the item to be added.
    If the key doesn't exist, it creates a new list.

    Args:
        key: The label (key) for the list in the session state (e.g., "dietary_restrictions").
        value: The string information (value) to add to the list.
        tool_context: The ADK tool context.

    Returns:
        A status message confirming the addition.
    """
    mem_dict = tool_context.state
    if key not in mem_dict:
        mem_dict[key] = []
    # Ensure the state item is a list
    if not isinstance(mem_dict[key], list):
        # Handle error or convert - converting existing value to a list with the new one
        mem_dict[key] = [mem_dict[key]]

    if value not in mem_dict[key]:
        mem_dict[key].append(value)
        return {"status": f'Added "{value}" to list "{key}"'}
    else:
        return {"status": f'"{value}" already exists in list "{key}"'}


# Define the memorize tool function
def memorize(key: str, value: str, tool_context: ToolContext) -> Dict[str, str]:  # Changed value type to str
    """
    Memorizes a piece of information as a key-value pair in the session state.
    Stores the value as a string.

    Args:
        key: The label (key) for the information to be stored (e.g., "user_goal", "fitness_level").
        value: The string information (value) to be stored.
        tool_context: The ADK tool context, providing access to session state.

    Returns:
        A status message confirming the storage.
    """
    mem_dict = tool_context.state
    mem_dict[key] = value
    return {"status": f'Stored "{key}": "{value}"'}


# Define the forget tool function (optional, but good practice)
def forget(key: str, tool_context: ToolContext, value: Optional[str] = None) -> Dict[str, str]:  # Changed value type to Optional[str]
    """
    Forgets a piece of information. If only key is provided, removes the entire key.
    If key and value are provided, removes the string value from the list associated with the key.

    Args:
        key: The label (key) of the information to forget.
        tool_context: The ADK tool context.
        value: The specific string value to remove from a list (optional).

    Returns:
        A status message confirming the removal.
    """
    mem_dict = tool_context.state
    if key not in mem_dict:
        return {"status": f'Key "{key}" not found in memory.'}

    if value is None:
        # Forget the entire key
        try:
            del mem_dict[key]
            return {"status": f'Removed key "{key}"'}
        except KeyError:
            return {"status": f'Key "{key}" not found in memory.'}  # Should not happen due to check above, but safe
    else:
        # Forget a specific value from a list
        if isinstance(mem_dict.get(key), list):
            try:
                mem_dict[key].remove(value)
                # If list becomes empty, optionally remove the key itself
                if not mem_dict[key]:
                    del mem_dict[key]
                    return {"status": f'Removed value "{value}" from "{key}" and the key itself as it became empty.'}
                return {"status": f'Removed value "{value}" from list "{key}"'}
            except ValueError:
                return {"status": f'Value "{value}" not found in list "{key}"'}
        else:
            # Handle case where key exists but is not a list, or doesn't exist
            if key in mem_dict:
                return {"status": f'Cannot remove specific value from non-list key "{key}"'}
            else:  # Should not happen due to initial check
                return {"status": f'Key "{key}" not found in memory.'}


def _set_initial_states(source: Dict[str, Any], target: State | dict[str, Any]):
    """
    Sets the initial session state given a JSON object of states.

    Args:
        source: A JSON object containing the initial state structure (e.g., from a scenario file).
        target: The session state object (or dict) to populate.
    """
    # Add system time if not present (optional, depends on needs)
    if constants.SYSTEM_TIME not in target:
        target[constants.SYSTEM_TIME] = str(datetime.now())

    if constants.PROGRAM_INITIALIZED not in target:
        target[constants.PROGRAM_INITIALIZED] = True

        target.update(source)

        program = source.get(constants.PROGRAM_KEY, {})
        if program:
            target[constants.PROGRAM_START_DATE] = program[constants.START_DATE]
            target[constants.PROGRAM_END_DATE] = program[constants.END_DATE]
            target[constants.PROGRAM_DATETIME] = program[constants.START_DATE]

    # Example: Extract specific fields if needed for quick access (like in travel concierge)
    # user_profile = source.get(constants.USER_PROFILE_KEY, {})
    # if user_profile:
    #     target[constants.USER_GOAL] = user_profile.get(constants.FITNESS_GOALS)


def _load_precreated_profile(callback_context: CallbackContext):
    """
    Sets up the initial state by loading a profile from a JSON file.
    Intended to be used as a `before_agent_callback` for the root agent.
    This gets called before the system instruction is constructed.

    Args:
        callback_context: The callback context provided by ADK.
    """
    data = {}
    try:
        with open(SAMPLE_SCENARIO_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            print(f"\nLoading Initial State from {SAMPLE_SCENARIO_PATH}: {json.dumps(data, indent=2)}\n")
    except FileNotFoundError:
        print(f"\nWarning: Scenario file not found at {SAMPLE_SCENARIO_PATH}. Starting with empty state.\n")
        # Initialize with a default empty structure if file not found
        data = {"state": {}}  # Or load from diet_empty_default.json structure if preferred
    except json.JSONDecodeError:
        print(f"\nError: Could not decode JSON from {SAMPLE_SCENARIO_PATH}. Starting with empty state.\n")
        data = {"state": {}}

    # Ensure 'state' key exists in the loaded data
    initial_state_data = data.get("state", {})
    _set_initial_states(initial_state_data, callback_context.state)