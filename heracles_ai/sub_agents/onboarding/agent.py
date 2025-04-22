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
"""Onboarding Agent definition."""

from google.adk.agents import Agent
from heracles_ai.tools.memory import memorize, memorize_list, forget

from . import prompt


onboarding_agent = Agent(
    model="gemini-2.0-flash-001",
    name="onboarding_agent",
    description="Onboarding agent for Heracles.AI, responsible for gathering user information, goals and preferences.",
    instruction=prompt.ONBOARDING_AGENT_INSTR,
    tools=[
        memorize,  # Register the memorize tool
        memorize_list,  # Register the memorize_list tool
        forget,  # Register the forget tool
    ],
)

# TODO(b/336705178): Implement before_agent_callback if needed for initial state loading.
# TODO(b/336705178): Implement after_agent_callback if needed for post-processing.
# TODO(b/336705178): Implement memory management if needed.
# TODO(b/336705178): Implement error handling if needed.
# TODO(b/336705178): Implement logging if needed.