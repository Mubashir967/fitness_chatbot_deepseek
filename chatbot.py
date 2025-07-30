import pandas as pd
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

load_dotenv()

# Load DeepSeek API Key
api_key = os.getenv("DEEPSEEK_API_KEY")

# Setup LLM (assuming DeepSeek is OpenAI-compatible)
llm = ChatOpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com/v1",  # ✅ your DeepSeek API base
    model="deepseek-chat",  # or r1t2 if required
    temperature=0.3
)

# Load your CSVs
meals_df = pd.read_csv("datasets/daily_food_nutrition.csv")

# Agent with allow_dangerous_code
meal_agent = create_pandas_dataframe_agent(
    llm=llm,
    df=meals_df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    handle_parsing_errors=True,
    allow_dangerous_code=True  # ✅ Required
)

def answer_question(query):
    return meal_agent.run(query)
