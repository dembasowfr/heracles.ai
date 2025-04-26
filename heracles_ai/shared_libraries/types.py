# Copyright 2025 Google LLC
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

"""Common data schema and types for travel-concierge agents."""

from typing import Optional, Union

from google.genai import types
from pydantic import BaseModel, Field


# Convenient declaration for controlled generation.
json_response_config = types.GenerateContentConfig(
    response_mime_type="application/json"
)

class CaloriesMacros(BaseModel):
    """A calories and macros breakdown."""
    calories: int = Field(description="Total calories")
    protein: int = Field(description="Total protein in grams")
    carbs: int = Field(description="Total carbs in grams")
    fat: int = Field(description="Total fat in grams")
    fiber: int = Field(description="Total fiber in grams")
    sugar: int = Field(description="Total sugar in grams")
    sodium: int = Field(description="Total sodium in milligrams")
    cholesterol: int = Field(description="Total cholesterol in milligrams")
    saturated_fat: int = Field(description="Total saturated fat in grams")
