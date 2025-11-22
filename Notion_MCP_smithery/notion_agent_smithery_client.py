# notion_agent_client_v2.py
# Notion 자동화 에이전트 (신형 MultiServerMCPClient 버전)

import os
import asyncio
from dotenv import load_dotenv, find_dotenv

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

# .env 파일 로드
load_dotenv(find_dotenv())

# ──────────────────────────────────────────────
# 1️⃣ 모델 초기화
# ──────────────────────────────────────────────


# ──────────────────────────────────────────────
# 2️⃣ MultiServerMCPClient 설정
# ──────────────────────────────────────────────



# ──────────────────────────────────────────────
# 3️⃣ 메인 실행 함수
# ──────────────────────────────────────────────
async def run():
    

    # ──────────────────────────────────────────────
    # 4️⃣ LangChain 에이전트 생성
    # ──────────────────────────────────────────────
    


# ──────────────────────────────────────────────
# 5️⃣ 대화형 챗봇 실행
# ──────────────────────────────────────────────
async def start_chatbot(agent):
    

    while True:
        



# ──────────────────────────────────────────────
# 6️⃣ 실행
# ──────────────────────────────────────────────
if __name__ == "__main__":
