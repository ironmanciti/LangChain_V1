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
model = init_chat_model("gpt-5-mini", model_provider="openai")
# model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

# ──────────────────────────────────────────────
# 2️⃣ MultiServerMCPClient 설정
# ──────────────────────────────────────────────
client = MultiServerMCPClient(
    {
        "notion": {
            "transport": "stdio",  # 표준 입력/출력 기반 MCP 서버 실행
            "command": "npx",
            "args": ["-y", "@notionhq/notion-mcp-server"],
            "env": {
                # Notion 공식 MCP 서버 인증용 환경변수
                "NOTION_TOKEN": os.getenv("NOTION_API_KEY", ""),
            },
        }
    }
)

# ──────────────────────────────────────────────
# 3️⃣ 메인 실행 함수
# ──────────────────────────────────────────────
async def run():
    print("🔗 Notion MCP 서버 연결 중...")

    # MCP 서버에서 도구 불러오기
    tools = await client.get_tools()
    print(f"✅ Notion MCP 서버 연결 완료 — 사용 가능한 도구 {len(tools)}개\n")

    # 도구 목록 출력
    print("📦 사용 가능한 Notion 도구 목록:")
    for i, tool in enumerate(tools, 1):
        print(f"  {i}. {tool.name}: {tool.description}")
    print()

    # ──────────────────────────────────────────────
    # 4️⃣ LangChain 에이전트 생성
    # ──────────────────────────────────────────────
    memory = MemorySaver()
    agent = create_agent(
        model=model,
        tools=tools,
        checkpointer=memory
    )

    print("🚀 Notion Agent 생성 완료")
    await start_chatbot(agent)

# ──────────────────────────────────────────────
# 5️⃣ 대화형 챗봇 실행
# ──────────────────────────────────────────────
async def start_chatbot(agent):
    default_page_id = os.getenv("NOTION_PAGE_ID", "")
    session_id = "notion_session"

    print("\n" + "=" * 60)
    print("💬 Notion 자동화 Agent 시작!")
    if default_page_id:
        print(f"기본 작업 페이지 ID: {default_page_id}")
    else:
        print("⚠️ .env 파일에 NOTION_PAGE_ID가 설정되지 않았습니다.")
    print("'quit' 또는 'exit'으로 종료")
    print("=" * 60 + "\n")

    while True:
        user_input = input("질문을 입력하세요: ")

        if user_input.lower() in ["quit", "exit", "종료"]:
            print("🛑 Notion Agent를 종료합니다.")
            break

        # 페이지 ID를 자동으로 사용자 입력에 포함
        enhanced_input = (
            f"{user_input}\n\n"
            f"[참고: 기본 작업 페이지 ID는 {default_page_id or '(없음)'}입니다.]"
        )

        user_message = HumanMessage(content=enhanced_input)
        config = {"configurable": {"thread_id": session_id}}

        print("🧠 처리 중...\n")
        response = await agent.ainvoke({"messages": [user_message]}, config=config)

        print("🤖 응답:")
        print(response["messages"][-1].content)
        print("\n" + "=" * 50 + "\n")


# ──────────────────────────────────────────────
# 6️⃣ 실행
# ──────────────────────────────────────────────
if __name__ == "__main__":
    try:
        asyncio.run(run())
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()