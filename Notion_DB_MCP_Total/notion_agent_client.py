# integrated_agent_client_v2.py
# 여러 MCP 서버(chinook, notion)를 MultiServerMCPClient로 통합하여 사용하는 예제

import os
import asyncio
from dotenv import load_dotenv

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

load_dotenv()

# 1) 모델 준비


# 2) MultiServerMCPClient로 두 MCP 서버(chinook, notion) 정의



async def run():
   


async def start_chatbot(agent):
    

    while True:
        



if __name__ == "__main__":
   