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
model = init_chat_model("gpt-5-mini", model_provider="openai")
# model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

# 2) MultiServerMCPClient로 두 MCP 서버(chinook, notion) 정의
client = MultiServerMCPClient(
    {
        "chinook": {
            "transport": "stdio",            # 로컬 서브프로세스(stdio)로 실행
            "command": "python",
            "args": ["../DB_MCP_Agent/xagent_server.py"],  # Chinook DB MCP 서버 스크립트 경로
        },
        "notion": {
            "transport": "stdio",            # npx 로 Notion 공식 MCP 서버 실행
            "command": "npx",
            "args": ["-y", "@notionhq/notion-mcp-server"],
            "env": {
                "NOTION_TOKEN": os.getenv("NOTION_API_KEY", ""),  # .env에 NOTION_API_KEY 필요
            },
        },
        # 필요하면 HTTP 기반 원격 MCP도 함께 붙일 수 있습니다:
        # "weather": {
        #     "transport": "streamable_http",
        #     "url": "http://localhost:8000/mcp"
        # }
    }
)

async def run():
    print("🔗 MCP 서버 연결 및 도구 수집 중...")
    # 3) 모든 등록 서버에서 Tool 수집 (자동 연결/초기화)
    tools = await client.get_tools()
    print(f"✅ 통합 도구 수집 완료: 총 {len(tools)}개\n")

    # 4) 에이전트 생성(메모리 포함)
    memory = MemorySaver()
    agent = create_agent(
        model=model,
        tools=tools,
        checkpointer=memory
    )
    print("🚀 통합 ReAct Agent 생성 완료")

    await start_chatbot(agent)

async def start_chatbot(agent):
    # Notion 기본 작업 페이지 ID (있으면 프롬프트에 자동 포함)
    default_page_id = os.getenv("NOTION_PAGE_ID", "")
    session_id = "integrated_session"

    print("\n" + "=" * 60)
    print("💬 통합 MCP Agent 시작! (Chinook + Notion)")
    if default_page_id:
        print(f"기본 Notion 페이지 ID: {default_page_id}")
    else:
        print("⚠️ .env에 NOTION_PAGE_ID가 없으므로, 페이지 작업 시 ID를 직접 입력해야 합니다.")
    print("'quit' 또는 'exit'으로 종료")
    print("=" * 60 + "\n")

    while True:
        user_input = input("질문을 입력하세요: ")
        if user_input.lower() in ["quit", "exit", "종료"]:
            print("\n🛑 통합 Agent를 종료합니다.")
            break

        # Notion 페이지 ID를 안내 문구로 주입(있을 때만)
        if default_page_id:
            enhanced_input = (
                f"{user_input}\n\n"
                f"[참고: Notion 작업 시 기본 부모 페이지 ID는 {default_page_id}입니다.]"
            )
        else:
            enhanced_input = user_input

        print("🧠 처리 중...\n")
        user_message = HumanMessage(content=enhanced_input)
        config = {"configurable": {"thread_id": session_id}}

        resp = await agent.ainvoke({"messages": [user_message]}, config=config)
        print("🤖 응답:")
        print(resp["messages"][-1].content)
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()