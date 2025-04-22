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
from heracles_ai.tools.nutrition import nutrition

from google.adk.agents import Agent


dietitian_agent = Agent(
    model="gemini-2.0-flash-001",
    name="dietitian_agent",
    description="Dietitian agent for Heracles.AI, responsible for providing personalized nutrition plans and feedback.",
    instruction=prompt.DIETITIAN_AGENT_INSTR,
    sub_agents=[
        # Add any sub-agents if needed
    ],
    tools=[
        memorize,  # Register the memorize tool
        nutrition,  # Use actual fitness_tool
    ],
)