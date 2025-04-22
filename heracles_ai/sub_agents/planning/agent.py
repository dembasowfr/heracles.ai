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
"""Planning Agent definition for Heracles.AI."""

# Import the Agent class
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

# Import the prompt for this agent
from . import prompt

# Import necessary tools
from heracles_ai.tools.memory import memorize  # Only import the specific tool needed
from heracles_ai.sub_agents.coach.agent import coach_agent  # Import the actual fitness tool
# from heracles_ai.sub_agents.dietitian.agent import dietitian_age  # Import the actual nutrition tool
from heracles_ai.sub_agents.dietitian.agent import dietitian_agent  # Import the actual nutrition tool
# TODO(b/336705178): Import actual tool instances once created
# from heracles_ai.tools.conversion import metric_conversion_tool


planning_agent = Agent(
    model="gemini-2.0-flash-001",
    name="planning_agent",
    description="Planning agent for Heracles.AI, responsible for creating personalized fitness and nutrition plans.",
    instruction=prompt.PLANNING_AGENT_INSTR,
    tools=[
        memorize,  # Register the memorize tool
        AgentTool(agent=coach_agent),
        AgentTool(agent=dietitian_agent),
    ],
)