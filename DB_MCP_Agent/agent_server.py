from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from contextlib import asynccontextmanager
from langchain_community.utilities import SQLDatabase
import os
import sys
import asyncio

# 전역 데이터베이스 연결 변수
# 서버 수명 주기 동안 유지되는 데이터베이스 연결 객체
db = None

@asynccontextmanager
async def lifespan(app):
    """
    서버 시작/종료 시 데이터베이스 연결 관리
    """
    

# FastMCP 서버 인스턴스 생성
# - "ChinookDBAnalysis": MCP 서버의 이름
# - lifespan: 서버 시작/종료 시 실행될 함수


@mcp.tool()
def execute_sql_query(query: str) -> str:
    """
    SQL 쿼리를 실행하고 결과를 반환합니다.
    """
    

@mcp.tool()
def get_table_schema(table_name: str) -> str:
    """
    특정 테이블의 컬럼명, 데이터 타입, 제약조건 등의
    스키마 정보를 조회합니다.
    """


@mcp.tool()
def list_tables() -> list:
    """
    현재 연결된 데이터베이스에서 사용 가능한
    모든 테이블의 이름을 리스트로 반환합니다.
    """


@mcp.tool()
def validate_sql_query(query: str) -> dict:
    """
    실제로 쿼리를 실행하지 않고 문법만 검증하여
    SQL 쿼리가 올바른지 확인합니다.
    """
    

@mcp.resource("database://info")
def get_database_info() -> dict:
    """
    Chinook 데이터베이스의 전반적인 정보를 반환합니다.
    MCP 리소스로 등록되어 클라이언트가 데이터베이스의
    기본 정보를 조회할 수 있습니다.
    
    Returns:
        dict: 데이터베이스 정보
              - database: 데이터베이스 이름
              - tables_count: 테이블 개수
              - tables: 테이블 목록 
              - description: 데이터베이스 설명
    """
    



@mcp.resource("table://{table_name}")
def get_table_info(table_name: str) -> str:
    """  
    MCP 리소스로 등록되어 동적 URI 패턴으로
    특정 테이블의 상세 정보를 반환합니다.    
    """
    


@mcp.prompt()
def default_prompt(message: str) -> list[base.Message]:
    """ 
    MCP 프롬프트로 등록되어 클라이언트가 대화를 시작할 때
    사용할 수 있는 시스템 메시지와 사용자 메시지를 반환합니다.
    """


if __name__ == "__main__":
    try:
        print("MCP Server is running...", file=sys.stderr)
        # stdio: 표준 입출력을 통해 클라이언트와 통신
        mcp.run(transport="stdio")
