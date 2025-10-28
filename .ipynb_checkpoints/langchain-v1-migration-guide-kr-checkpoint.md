# LangChain v1 마이그레이션 가이드

이 가이드는 [LangChain v1](/oss/python/releases/langchain-v1)과 이전 버전 간의 주요 변경 사항을 설명합니다.

## 간소화된 패키지

v1에서 `langchain` 패키지 네임스페이스가 에이전트를 위한 필수 빌딩 블록에 초점을 맞추기 위해 크게 축소되었습니다. 간소화된 패키지로 핵심 기능을 더 쉽게 찾고 사용할 수 있습니다.

### 네임스페이스

| 모듈                                                                                   | 사용 가능한 항목                                                                                                                                                                                                                                                          | 참고사항                          |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| [`langchain.agents`](https://reference.langchain.com/python/langchain/agents)         | [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent), [`AgentState`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.AgentState)                                                            | 핵심 에이전트 생성 기능 |
| [`langchain.messages`](https://reference.langchain.com/python/langchain/messages)     | 메시지 타입, [콘텐츠 블록](https://reference.langchain.com/python/langchain/messages/#langchain.messages.ContentBlock), [`trim_messages`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.trim_messages)                               | `langchain-core`에서 재내보냄 |
| [`langchain.tools`](https://reference.langchain.com/python/langchain/tools)           | [`@tool`](https://reference.langchain.com/python/langchain/tools/#langchain.tools.tool), [`BaseTool`](https://reference.langchain.com/python/langchain/tools/#langchain.tools.BaseTool), 주입 헬퍼                                                                | `langchain-core`에서 재내보냄 |
| [`langchain.chat_models`](https://reference.langchain.com/python/langchain/models)    | [`init_chat_model`](https://reference.langchain.com/python/langchain/models/#langchain.chat_models.init_chat_model), [`BaseChatModel`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel)   | 통합 모델 초기화      |
| [`langchain.embeddings`](https://reference.langchain.com/python/langchain/embeddings) | [`init_embeddings`](https://reference.langchain.com/python/langchain_core/embeddings/#langchain_core.embeddings.embeddings.Embeddings), [`Embeddings`](https://reference.langchain.com/python/langchain_core/embeddings/#langchain_core.embeddings.embeddings.Embeddings) | 임베딩 모델                  |

### `langchain-classic`

`langchain` 패키지에서 다음 중 하나를 사용하고 있었다면, [`langchain-classic`](https://pypi.org/project/langchain-classic/)을 설치하고 import를 업데이트해야 합니다:

* 레거시 체인 (`LLMChain`, `ConversationChain` 등)
* 리트리버 (예: `MultiQueryRetriever` 또는 이전 `langchain.retrievers` 모듈의 모든 것)
* 인덱싱 API
* 허브 모듈 (프롬프트를 프로그래밍 방식으로 관리하기 위한)
* 임베딩 모듈 (예: `CacheBackedEmbeddings` 및 커뮤니티 임베딩)
* [`langchain-community`](https://pypi.org/project/langchain-community) 재내보내기
* 기타 더 이상 사용되지 않는 기능

<CodeGroup>
  ```python v1 (새 버전) theme={null}
  # 체인
  from langchain_classic.chains import LLMChain

  # 리트리버
  from langchain_classic.retrievers import ...

  # 인덱싱
  from langchain_classic.indexes import ...

  # 허브
  from langchain_classic import hub
  ```

  ```python v0 (이전 버전) theme={null}
  # 체인
  from langchain.chains import LLMChain

  # 리트리버
  from langchain.retrievers import ...

  # 인덱싱
  from langchain.indexes import ...

  # 허브
  from langchain import hub
  ```
</CodeGroup>

설치 방법:

<CodeGroup>
  ```bash pip theme={null}
  pip install langchain-classic
  ```

  ```bash uv theme={null}
  uv add langchain-classic
  ```
</CodeGroup>

***

## `create_agent`로 마이그레이션

v1.0 이전에는 에이전트를 구축하기 위해 `langgraph.prebuilt.create_react_agent` 사용을 권장했습니다.
이제는 에이전트를 구축하기 위해 [`langchain.agents.create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent)를 사용하는 것을 권장합니다.

아래 표는 `create_react_agent`에서 [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent)로 변경된 기능을 설명합니다:

| 섹션                                            | 요약 - 변경 사항                                                                                                                                                                     |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Import 경로](#import-경로)                        | 패키지가 `langgraph.prebuilt`에서 `langchain.agents`로 이동                                                                                                                              |
| [프롬프트](#프롬프트)                                | 매개변수 이름이 [`system_prompt`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent\(system_prompt\))로 변경, 동적 프롬프트는 미들웨어 사용            |
| [모델 전 훅](#모델-전-훅)                  | `before_model` 메서드가 있는 미들웨어로 대체                                                                                                                                          |
| [모델 후 훅](#모델-후-훅)                | `after_model` 메서드가 있는 미들웨어로 대체                                                                                                                                           |
| [사용자 정의 상태](#사용자-정의-상태)                      | `TypedDict`만 사용, [`state_schema`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.AgentMiddleware.state_schema) 또는 미들웨어를 통해 정의 가능 |
| [모델](#모델)                                    | 미들웨어를 통한 동적 선택, 사전 바인딩된 모델은 지원되지 않음                                                                                                                           |
| [도구](#도구)                                    | 도구 오류 처리가 `wrap_tool_call`이 있는 미들웨어로 이동                                                                                                                              |
| [구조화된 출력](#구조화된-출력)            | 프롬프트 출력 제거, `ToolStrategy`/`ProviderStrategy` 사용                                                                                                                             |
| [스트리밍 노드 이름](#스트리밍-노드-이름-변경) | 노드 이름이 `"agent"`에서 `"model"`로 변경                                                                                                                                              |
| [런타임 컨텍스트](#런타임-컨텍스트)                | `config["configurable"]` 대신 `context` 인자를 통한 의존성 주입                                                                                                            |
| [네임스페이스](#간소화된-네임스페이스)                 | 에이전트 빌딩 블록에 초점을 맞추기 위해 간소화, 레거시 코드는 `langchain-classic`으로 이동                                                                                                    |

### Import 경로

에이전트 프리빌트의 import 경로가 `langgraph.prebuilt`에서 `langchain.agents`로 변경되었습니다.
함수 이름이 `create_react_agent`에서 [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent)로 변경되었습니다:

```python  theme={null}
from langgraph.prebuilt import create_react_agent # [!code --]
from langchain.agents import create_agent # [!code ++]
```

자세한 정보는 [에이전트](/oss/python/langchain/agents)를 참조하세요.

### 프롬프트

#### 정적 프롬프트 이름 변경

`prompt` 매개변수가 [`system_prompt`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent\(system_prompt\))로 이름이 변경되었습니다:

<CodeGroup>
  ```python v1 (새 버전) theme={null}
  from langchain.agents import create_agent


  agent = create_agent(
      model="anthropic:claude-sonnet-4-5",
      tools=[check_weather],
      system_prompt="You are a helpful assistant"  # [!code highlight]
  )
  ```

[문서가 매우 길어서 일부만 번역했습니다. 계속 번역이 필요하시면 말씀해 주세요.]

## 중단된 변경 사항

### Python 3.9 지원 중단

모든 LangChain 패키지는 이제 **Python 3.10 이상**이 필요합니다. Python 3.9는 2025년 10월에 [수명 종료](https://devguide.python.org/versions/)됩니다.

### 채팅 모델의 반환 타입 업데이트

채팅 모델 호출의 반환 타입 시그니처가 [`BaseMessage`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.messages.BaseMessage)에서 [`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage)로 수정되었습니다. [`bind_tools`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.bind_tools)를 구현하는 사용자 정의 채팅 모델은 반환 시그니처를 업데이트해야 합니다:

<CodeGroup>
  ```python v1 (새 버전) theme={null}
  def bind_tools(
          ...
      ) -> Runnable[LanguageModelInput, AIMessage]:
  ```

  ```python v0 (이전 버전) theme={null}
  def bind_tools(
          ...
      ) -> Runnable[LanguageModelInput, BaseMessage]:
  ```
</CodeGroup>

### OpenAI Responses API의 기본 메시지 형식

Responses API와 상호작용할 때, `langchain-openai`는 이제 응답 항목을 메시지 `content`에 저장하는 것이 기본값입니다. 이전 동작을 복원하려면 `LC_OUTPUT_VERSION` 환경 변수를 `v0`로 설정하거나 [`ChatOpenAI`](https://reference.langchain.com/python/integrations/langchain_openai/ChatOpenAI/)를 인스턴스화할 때 `output_version="v0"`를 지정하세요.

```python  theme={null}
# output_version 플래그로 이전 동작 강제
model = ChatOpenAI(model="gpt-4o-mini", output_version="v0")
```

### `langchain-anthropic`의 기본 `max_tokens`

`langchain-anthropic`의 `max_tokens` 매개변수는 이제 이전 기본값인 `1024` 대신 선택한 모델에 따라 더 높은 값으로 기본 설정됩니다. 이전 기본값에 의존했다면 명시적으로 `max_tokens=1024`를 설정하세요.

### 레거시 코드가 `langchain-classic`으로 이동

표준 인터페이스와 에이전트에 초점을 벗어난 기존 기능은 [`langchain-classic`](https://pypi.org/project/langchain-classic) 패키지로 이동되었습니다. 핵심 `langchain` 패키지에서 사용 가능한 내용과 `langchain-classic`으로 이동한 내용에 대한 자세한 내용은 [간소화된 네임스페이스](#간소화된-네임스페이스) 섹션을 참조하세요.

### 더 이상 사용되지 않는 API 제거

이미 더 이상 사용되지 않고 1.0에서 제거 예정이었던 메서드, 함수 및 기타 객체가 삭제되었습니다. 교체 API에 대해서는 이전 버전의 [사용 중단 공지](https://python.langchain.com/docs/versions/migrating_chains)를 확인하세요.

### `.text()`가 이제 속성입니다

메시지 객체에서 `.text()` 메서드 사용 시 괄호를 제거해야 합니다:

```python  theme={null}
# 속성 접근
text = response.text

# 더 이상 사용되지 않는 메서드 호출
text = response.text()
```

기존 사용 패턴(즉, `.text()`)은 계속 작동하지만 이제 경고를 발생시킵니다.

***

<Callout icon="pen-to-square" iconType="regular">
  [GitHub에서 이 페이지의 소스를 편집하세요.](https://github.com/langchain-ai/docs/edit/main/src/oss/python/migrate/langchain-v1.mdx)
</Callout>

<Tip icon="terminal" iconType="regular">
  실시간 답변을 위해 MCP를 통해 이 문서들을 Claude, VSCode 등에 [프로그래밍 방식으로 연결](/use-these-docs)하세요.
</Tip>
