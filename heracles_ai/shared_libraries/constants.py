# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in wrPROGRAMg, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Constants used as keys into ADK's session state."""

SYSTEM_TIME = "_time"
PROGRAM_INITIALIZED = "_program_initialized"

PROGRAM_KEY = "program"
PROFILE_KEY = "user_profile"

PROGRAM_START_DATE = "program_start_date"
PROGRAM_END_DATE = "program_end_date"
PROGRAM_DATETIME = "program_datetime"

START_DATE = "start_date"
END_DATE = "end_date"


# Activity level multipliers for TDEE calculation
ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,         # Little or no exercise
    "lightly_active": 1.375,   # Light exercise/sports 1-3 days/week
    "moderately_active": 1.55, # Moderate exercise/sports 3-5 days/week
    "very_active": 1.725,     # Hard exercise/sports 6-7 days a week
    "extra_active": 1.9       # Very hard exercise/sports & physical job
}

# Calorie adjustments based on goal
GOAL_ADJUSTMENTS = {
    "lose_weight": -500,    # Deficit for weight loss
    "maintain_weight": 0,   # No adjustment for maintenance
    "gain_weight": 500      # Surplus for weight gain
}