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
#
# pylint: disable=line-too-long
"""Coach Agent definition for Heracles.AI."""


# Import the prompt for this agent
from . import prompt
from heracles_ai.tools.memory import memorize  # Only import the specific tool needed
# Import necessary tools
from heracles_ai.tools.nutrition import nutrition_tool
from heracles_ai.tools.cmc import calories_macro_calculator_tool
from google.adk.tools.agent_tool import AgentTool
from heracles_ai.shared_libraries import types


from google.adk.agents import Agent


nutiritions_calculator_agent = Agent(
    model="gemini-2.0-flash-001",
    name="nutiritions_calculator_agent",
    description="CMC agent for Heracles.AI, responsible for calculating calories and macros.",
    instruction=prompt.CMC_AGENT_INSTR,
    #output_schema= types.CaloriesMacros,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_key= "cmc",
    tools=[
        memorize,  # Register the memorize tool
        calories_macro_calculator_tool,  # Add the calorie calculation tool
    ],
)

dietitian_agent = Agent(
    model="gemini-2.0-flash-001",
    name="dietitian_agent",
    description="Dietitian agent for Heracles.AI, responsible for providing personalized nutrition plans and feedback.",
    instruction=prompt.DIETITIAN_AGENT_INSTR,

    tools=[
        AgentTool(agent=nutiritions_calculator_agent),
        memorize,  # Register the memorize tool
        nutrition_tool,  # Use actual fitness_tool
    ],
)