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

"""Monitoring Agent definition."""

from google.adk.agents import Agent

# Assuming memory tool is needed for accessing user plans/history
from heracles_ai.tools.memory import memorize
from . import prompt

monitoring_agent = Agent(
    # Use a model compatible with the live API
    model="gemini-2.0-flash-001",
    name="monitoring_agent",
    description="Monitors user adherence to fitness and diet plans by asking questions.",
    instruction=prompt.MONITORING_AGENT_INSTR,
    tools=[memorize],  # Add memory tool to access plans and history
)