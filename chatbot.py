from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd
import os
from dotenv import load_dotenv

# Load the API key
load_dotenv()

# Load your datasets
meals_df = pd.read_csv("datasets/daily_food_nutrition.csv")
exercises_df = pd.read_csv("datasets/exercise_dataset.csv")
injuries_df = pd.read_csv("datasets/injury_data.csv")

# Create dataframe agents
meals_agent = create_pandas_dataframe_agent(
    ChatOpenAI(
        temperature=0,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        model="mistralai/mistral-7b-instruct"  # You can change to other models
    ),
    meals_df,
    verbose=True
)

exercise_agent = create_pandas_dataframe_agent(
    ChatOpenAI(
        temperature=0,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        model="mistralai/mistral-7b-instruct"
    ),
    exercises_df,
    verbose=True
)

injury_agent = create_pandas_dataframe_agent(
    ChatOpenAI(
        temperature=0,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        model="mistralai/mistral-7b-instruct"
    ),
    injuries_df,
    verbose=True
)

# Define tools
tools = [
    Tool(name="Meal Plan Tool", func=meals_agent.run, description="Provides meal plans"),
    Tool(name="Workout Tool", func=exercise_agent.run, description="Suggests workouts"),
    Tool(name="Injury Prevention Tool", func=injury_agent.run, description="Helps with injury prevention"),
]

# Initialize agent
agent = initialize_agent(
    tools, 
    ChatOpenAI(
        temperature=0,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        model="mistralai/mistral-7b-instruct"
    ),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Define response function
def get_bot_response(user_message):
    return agent.run(user_message)
