\
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
"""Heracles.AI Root Agent definition."""

from google.adk.agents import Agent

from heracles_ai import prompt

# import onboarding_agent
from heracles_ai.sub_agents.onboarding.agent import onboarding_agent
from heracles_ai.sub_agents.planning.agent import planning_agent
from heracles_ai.tools.memory import _load_precreated_profile
# TODO(b/336705178): Import and register sub-agents.
# TODO(b/336705178): Import and register tools.
# TODO(b/336705178): Implement before_agent_callback if needed for initial state loading.

from heracles_ai.sub_agents.coach.agent import coach_agent  # Import the actual fitness tool
from heracles_ai.sub_agents.dietitian.agent import dietitian_agent  # Import the actual nutrition tool
from heracles_ai.sub_agents.monitoring.agent import monitoring_agent # Import the monitoring agent
from heracles_ai.sub_agents.feedback.agent import feedback_agent # Import the feedback agent

from heracles_ai.tools.memory import memorize  # Only import the specific tool needed

root_agent = Agent(
    model="gemini-2.0-flash-001", # Updated model
    name="root_agent",
    description="Heracles.ai: A Health and Fitness Coach using the services of multiple sub-agents",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        onboarding_agent,
        planning_agent,
        coach_agent,
        dietitian_agent,
        monitoring_agent, # Added monitoring agent
        feedback_agent,   # Added feedback agent
    ],
    tools=[
        memorize
    ],
    before_agent_callback=_load_precreated_profile,
)