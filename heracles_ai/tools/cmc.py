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

"""Tool for calculating estimated daily calorie and macronutrient needs
and providing workout guidance."""

from typing import Dict, Any
import google.adk.tools as ToolContext
from heracles_ai.shared_libraries.constants import (
    ACTIVITY_MULTIPLIERS,
    GOAL_ADJUSTMENTS
)


def calories_macro_calculator_tool(query: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Calculates estimated daily calorie and macronutrient needs based on user
    profile and goals, and provides general workout guidance.

    Uses the Mifflin-St Jeor formula for BMR and adjusts based on activity level
    and fitness goal (lose, maintain, gain weight). Also calculates protein,
    carbohydrate, and fat recommendations.

    Args:
        query: The user query (not directly used for calculation but required by ADK).
        tool_context: The ADK tool context containing session state with user profile.

    Returns:
        A dictionary containing the estimated daily calorie needs, macronutrient
        recommendations, workout guidance, or an error message.
    """
    print(f"[calculate_comprehensive_needs] Received query: {query}")
    # --- Access session state via tool_context.session_state ---
    user_profile = tool_context.state.get("user_profile")
    if not user_profile:
        return {"error": "User profile not found in session state. Please provide user profile information."}
    # --- End state access ---

    # --- Extract required user data ---
    try:
        # Check if user_profile is a dictionary before proceeding
        if not isinstance(user_profile, dict):
            print(f"[calculate_comprehensive_needs] Error: user_profile is not a dictionary (type: {type(user_profile)})" )
            return {"error": "Internal error: Retrieved user profile is not in the expected format."}

        # --- Existing extraction and validation logic ---
        age_str = user_profile.get("age")
        sex_str = user_profile.get("sex")
        height_str = user_profile.get("height_cm")
        weight_str = user_profile.get("weight_kg")
        activity_level_raw = str(user_profile.get("activity_level", "")).lower()
        goal_raw = user_profile.get("fitness_goals", [])
        diet_prefs = user_profile.get("dietary_preferences", [])

        # --- Type Conversion and Validation ---
        try:
            # --- Add check for empty strings before conversion --- 
            if not age_str:
                raise ValueError("Age is missing or empty in user profile")
            if not height_str:
                raise ValueError("Height (cm) is missing or empty in user profile")
            if not weight_str:
                raise ValueError("Weight (kg) is missing or empty in user profile")
            # --- End check --- 
            
            age = int(age_str)
            sex = str(sex_str).lower() if sex_str else "male" # Default to male
            height_cm = float(height_str)
            weight_kg = float(weight_str)
        except (ValueError, TypeError) as e:
            print(f"[calculate_comprehensive_needs] Error converting profile values: {e}")
            # Re-raise or return a more specific error based on the caught exception
            return {"error": f"Invalid format or missing value in user profile data (age, height, weight). Please ensure they are provided and are valid numbers. Details: {e}"}

        # --- Validate other fields ---
        activity_level = activity_level_raw
        goal = str(goal_raw).lower().replace(" ", "_") # e.g., "lose weight" -> "lose_weight"

        if not all([age, sex, height_cm, weight_kg, activity_level, goal]):
            missing = [k for k, v in user_profile.items() if not v]
            return {"error": f"Missing required user profile information: {missing}. Please provide age, sex, height (cm), weight (kg), activity level, and goal."}

        if sex not in ["male", "female"]:
            return {"error": f"Invalid sex specified: '{sex}'. Must be 'male' or 'female'."}
        if activity_level not in ACTIVITY_MULTIPLIERS:
            return {"error": f"Invalid activity level: '{activity_level}'. Valid levels are: {list(ACTIVITY_MULTIPLIERS.keys())}"}
        if goal not in GOAL_ADJUSTMENTS:
            return {"error": f"Invalid goal: '{goal}'. Valid goals are: {list(GOAL_ADJUSTMENTS.keys())}"}

    except Exception as e: # Catch broader errors during extraction/parsing
        print(f"[calculate_comprehensive_needs] Error parsing user profile: {e}")
        return {"error": f"Could not parse user profile data. Ensure age, height, and weight are numbers. Error: {e}"}

    print(f"[calculate_comprehensive_needs] Calculating for: Age={age}, Sex={sex}, H={height_cm}cm, W={weight_kg}kg, Activity={activity_level}, Goal={goal}")

    # --- Calculate BMR using Mifflin-St Jeor ---
    if sex == "male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else: # female
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    # --- Calculate TDEE ---
    activity_multiplier = ACTIVITY_MULTIPLIERS[activity_level]
    tdee = bmr * activity_multiplier

    # --- Adjust for Goal (Calories) ---
    goal_adjustment = GOAL_ADJUSTMENTS[goal]
    estimated_daily_calories = round(tdee + goal_adjustment)

    # --- Calculate Macronutrient Needs (General Guidelines) ---
    protein_grams = round(1.6 * weight_kg) # Aim for 1.6 g/kg for general fitness
    if goal == "gain_weight":
        protein_grams = round(1.8 * weight_kg) # Slightly higher for muscle growth
    elif goal == "lose_weight":
        protein_grams = round(1.8 * weight_kg) # To preserve muscle mass

    # Carbohydrates and Fats (Adjust based on activity and preference)
    # These are starting points and can be adjusted based on the user's response
    # to the plan and their preferences.
    if activity_level in ["sedentary", "lightly_active"]:
        fat_grams = round(1.0 * weight_kg)
        carb_grams = round((estimated_daily_calories - (protein_grams * 4) - (fat_grams * 9)) / 4)
    else: # More active
        fat_grams = round(0.8 * weight_kg)
        carb_grams = round((estimated_daily_calories - (protein_grams * 4) - (fat_grams * 9)) / 4)

    # Ensure carb_grams is not negative
    carb_grams = max(0, carb_grams)

    # --- Provide General Workout Guidance based on Goal ---

    print(f"[calculate_comprehensive_needs] BMR={bmr:.2f}, TDEE={tdee:.2f}, Adjustment={goal_adjustment}, Final Calories={estimated_daily_calories}")
    print(f"[calculate_comprehensive_needs] Protein={protein_grams}g, Carbs={carb_grams}g, Fats={fat_grams}g")

    return {
        "estimated_daily_calories": estimated_daily_calories,
        "protein_grams": protein_grams,
        "carbohydrate_grams": carb_grams,
        "fat_grams": fat_grams,
        "calculation_details": {
            "bmr": round(bmr, 2),
            "tdee": round(tdee, 2),
            "goal_adjustment": goal_adjustment,
            "activity_level": activity_level,
            "goal": goal
        }
    }