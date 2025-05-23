# 📋 Heracles.AI — Your Personal Health and Fitness Coach

![Heracles.AI](general-architecture.jpg)

Heracles.AI is a **multi-agent system** designed to assist users in achieving their health and fitness goals. It provides personalized coaching, nutrition advice, and progress tracking through a collaborative network of specialized agents.


A cohort of specialized agents mimics the experience of having a personal health and fitness coach, guiding users through their wellness journey:

- Understanding goals and current state
- Planning personalized routines and nutrition
- Providing support during activities
- Monitoring progress
- Adapting strategies for long-term success

This example illustrates the use of **ADK-supported tools** such as **Google Search Grounding** and the concept of **managing state as memory**.

---

## 📖 Overview

<img src="heracles-ai-architecture.svg" alt="Heracles.AI Architecture"/>

A user's health and fitness journey can be divided into several stages:

1. **Onboarding**
2. **Planning & Guidance**
3. **Execution & Support**
4. **Progress Monitoring**
5. **Long-term Engagement**

Each stage involves a **team of specialized agents** working collaboratively to provide a comprehensive coaching experience:

- **Onboarding stage**: Agents gather the user's goals, fitness level, dietary restrictions, lifestyle, and available resources.
- **Planning stage**: Personalized workout routines, nutrition plans, and well-being strategies are generated. This agent uses 2 other sub-agents **Dietitian** and **Coach** agents.
- **Progress Monitoring stage**: Agents track progress and suggest adjustments.
- **Feedback stage**: Agents gather insights and refine future plans.

---

## 🤖 Agent Details

**Key Features:**

| Feature            | Description            |
|:------------------|:----------------------|
| Interaction Type   | Conversational         |
| Complexity         | Advanced               |
| Agent Type         | Multi-Agent            |
| Components         | Tools, Memory          |
| Vertical           | Health & Fitness       |

---

## 🏛️ Agent Architecture

**Heracles.AI Multi-Agent Folder Structure**

```
heracles_ai/
├── shared_libraries/
│   ├── constants.py
│   └── types.py
├── sub_agents/
│   ├── __pycache__/
│   ├── coach/
│   ├── dietitian/
│   ├── feedback/
│   ├── monitoring/
│   ├── onboarding/
│   ├── planning/
│   └── __init__.py
└── tools/
    ├── __pycache__/
    ├── __init__.py
    ├── fitness.py
    ├── memory.py
    ├── nutrition.py
    ├── search.py
    └── cmc.py
├── agent.py
├── prompt.py

```

---

## 🧩 Component Details

### 📌 Sub-Agents

- **onboarding/onboarding_agent.py**  
  Interacts with the user to gather goals, current state, dietary restrictions, lifestyle, and resources.

- **planning/planning_agent.py**  
  Generates personalized workout, nutrition, and wellness strategies.

- **coach/coach_agent.py**  
  Provides workout guidance, technique advice, and answers questions.

- **dietitian/dietitian_agent.py**  
  Offers nutritional advice, meal planning, and dietary consultations.

- **monitoring/monitoring_agent.py**  
  Tracks user progress, identifies challenges, and suggests plan adjustments.

- **feedback/feedback_agent.py**  
  Collects feedback, improves future plans, ensures long-term engagement.


---

### 🛠️ Tools

- **tools/memory.py**  
  Manages state, user preferences, goals, and progress.

- **tools/search.py**  
  Integrates with Google Search Grounding to retrieve fitness and health data.

- **tools/exercise.py**  
  Manages exercise data, interfaces with exercise databases.

- **tools/fitness.py**  
  Contains general fitness-related utilities.

- **tools/nutrition.py**  
  Provides detailed nutrition logic and data.

- **tools/cmc.py**:
  Utilize Miffin-St Jeor equation for calculating Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE).
---

### 📚 Shared Libraries

- **shared_libraries/constants.py**  
  Project-wide constants (API keys, defaults, templates).

- **shared_libraries/types.py**  
  Custom data structures and Pydantic schemas.

---

## 🖥️ Setup and Installation

**Folder Structure**

(see **Agent Architecture** section above)

---

### ✅ Prerequisites

- **Python 3.11+**
- **Google Cloud Project** (for Vertex AI integration)
- **Google Agent Development Kit 1.0+**
- **Poetry**

**Install Poetry:**  
[Poetry Installation Guide](https://python-poetry.org/docs/#installation)

---

### 📥 Installation

1. **Clone the repository:**
   ```bash
   git clone <your_repository_url>
   cd <your_repository_directory>
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```

3. **Set up Google Cloud credentials**

   - Create a `.env` file:
     ```bash
     cp .env.example .env
     ```

   - Set the following environment variables:

     ```bash
     GOOGLE_GENAI_USE_VERTEXAI=1
     GOOGLE_CLOUD_PROJECT=__YOUR_CLOUD_PROJECT_ID__
     GOOGLE_CLOUD_LOCATION=us-central1
     GOOGLE_CLOUD_STORAGE_BUCKET=YOUR_BUCKET_NAME_HERE
     HERACLES_AI_SCENARIO=eval/program_empty_default.json
     ```

4. **Authenticate your Google account:**
   ```bash
   gcloud auth application-default login
   ```

5. **Activate Virtual Environment (Windows)**

   - Run:
     ```bash
     poetry env activate
     ```

   - Copy the activation path from the output:
     ```bash
     & "C:\Users\user\AppData\Local\pypoetry\Cache\virtualenvs\heracles-x2DohdsY-py3.12\Scripts\activate.ps1"
     ```

---

### 🛑 Possible Issues & Solutions

- **Permission Error (Activation)**  
  → Adjust **Local Security Policy** to create symbolic links for your user account.

- **Google API Errors (Missing Keys)**  
  Set environment variables manually:
  ```bash
  $env:GOOGLE_GENAI_USE_VERTEXAI = "1"
  $env:GOOGLE_CLOUD_PROJECT = "your-gcp-project-id"
  $env:GOOGLE_CLOUD_LOCATION = "your-gcp-region"
  $env:VERTEXAI = "true"
  ```

---

## 🏃 Running the Agent

**Using ADK**

- **Run via CLI:**
  ```bash
  adk run heracles_ai
  ```

- **Run via Web Interface:**
  ```bash
  adk web
  ```

  Open the URL, select `"heracles_ai"`, and chat with the agent.

---

## 🖥️ Programmatic Access (API)

**Start a Dev API Server**
```bash
adk api_server heracles_ai
```
→ Access: `http://127.0.0.1:8000/docs`

**Python Example**
```python
import requests, json

url = "http://127.0.0.1:8000/converse"

def interact(user_input):
    payload = {"user_input": user_input, "session_id": "test_session"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload))
    return response.json()

user_query = "What's a good workout for beginners?"
agent_response = interact(user_query)
print(f"[User]: {user_query}")
print(f"[Heracles.AI]: {agent_response['response']}")
```

---

## 💬 Sample Agent Interaction

**Example:**
```
[user]: I want to start working out to lose weight. I have some dumbbells at home.

[onboarding_agent]: Great! Could you tell me how many days a week you're available and for how long? Any dietary restrictions or preferences?

[user]: 3 days a week, 45 minutes. I'm vegetarian.

[planning_agent]: Here’s a workout and meal plan tailored for you...

[motivation_agent]: Awesome! Stay consistent. Let me know how it goes!
```

---

## 🌱 Worth Trying

**Complex Query Example**
```
I want a 4-day workout plan to build muscle at home using dumbbells and resistance bands. 
I'm also trying to eat healthier and need some vegetarian meal ideas for the week, focusing on high protein.
Can you give me a sample plan?
```
→ See how multiple agents collaborate in response.

---

## 🧪 Running Tests

- **Install Dev Dependencies**
  ```bash
  poetry install --with dev
  ```

- **Run Unit Tests**
  ```bash
  pytest
  ```

- **Specific Test**
  ```bash
  pytest tests/unit/onboarding/
  ```

- **Evaluate Overall Agent Behavior**
  ```bash
  pytest eval/
  ```

---

## 🚀 Deploying the Agent

**Install Deployment Dependencies**
```bash
poetry install --with deployment
```

**Deploy**
```bash
python deployment/deploy.py --create
```
→ Note down the **AgentEngine resource ID**.

**Quick Test**
```bash
python deployment/deploy.py --quicktest --resource_id=your_agent_engine_id --user_input="Tell me a beginner workout."
```

---

## 🔮 Future Development

This is an early version of Heracles.AI. We are actively working on enhancing its capabilities. Future improvements may include:

- Integration with more fitness tracking APIs (e.g., wearables, fitness apps).
- Expanded nutrition databases and API connections.
- Persistent database storage for long-term user progress and history.
- More sophisticated personalization algorithms.
- Enhanced natural language understanding for more complex interactions.

Stay tuned for updates!
