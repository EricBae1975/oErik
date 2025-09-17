#!/usr/bin/env python3
"""
Opik Python SDK LLM 통합 예제

이 예제는 Opik SDK를 사용하여 다양한 LLM 제공업체와 통합하는 방법을 보여줍니다.
"""

import opik
import os
from typing import Dict, Any, List

def openai_integration_example():
    """
    OpenAI 통합 예제
    """
    print("🤖 OpenAI 통합 예제...")
    
    try:
        # OpenAI 클라이언트 생성 (실제 API 키 필요)
        import openai
        
        # OpenAI 클라이언트를 Opik으로 추적
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-openai-api-key"))
        tracked_client = opik.integrations.openai.track_openai(client)
        
        # 추적된 클라이언트로 채팅 완성 요청
        response = tracked_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Explain artificial intelligence in simple terms"}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        print(f"✅ OpenAI 응답: {response.choices[0].message.content}")
        return True
        
    except ImportError:
        print("⚠️  OpenAI 라이브러리가 설치되지 않았습니다.")
        print("   pip install openai")
        return False
    except Exception as e:
        print(f"❌ OpenAI 통합 실패: {e}")
        return False

def anthropic_integration_example():
    """
    Anthropic 통합 예제
    """
    print("\n🧠 Anthropic 통합 예제...")
    
    try:
        # Anthropic 클라이언트 생성 (실제 API 키 필요)
        import anthropic
        
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", "your-anthropic-api-key"))
        tracked_client = opik.integrations.anthropic.track_anthropic(client)
        
        # 추적된 클라이언트로 메시지 요청
        response = tracked_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=150,
            messages=[
                {"role": "user", "content": "What is machine learning?"}
            ]
        )
        
        print(f"✅ Anthropic 응답: {response.content[0].text}")
        return True
        
    except ImportError:
        print("⚠️  Anthropic 라이브러리가 설치되지 않았습니다.")
        print("   pip install anthropic")
        return False
    except Exception as e:
        print(f"❌ Anthropic 통합 실패: {e}")
        return False

def langchain_integration_example():
    """
    LangChain 통합 예제
    """
    print("\n🔗 LangChain 통합 예제...")
    
    try:
        # LangChain 컴포넌트 생성
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage
        from langchain_core.prompts import ChatPromptTemplate
        
        # Opik 트레이서 생성
        tracer = opik.integrations.langchain.OpikTracer()
        
        # LangChain 체인 생성
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY", "your-openai-api-key")
        )
        
        # 프롬프트 템플릿 생성
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant."),
            ("human", "{question}")
        ])
        
        # 체인 생성
        chain = prompt | llm
        
        # Opik 트레이서로 체인 실행
        response = chain.invoke(
            {"question": "Explain deep learning"},
            config={"callbacks": [tracer]}
        )
        
        print(f"✅ LangChain 응답: {response.content}")
        return True
        
    except ImportError:
        print("⚠️  LangChain 라이브러리가 설치되지 않았습니다.")
        print("   pip install langchain langchain-openai")
        return False
    except Exception as e:
        print(f"❌ LangChain 통합 실패: {e}")
        return False

def litellm_integration_example():
    """
    LiteLLM 통합 예제
    """
    print("\n⚡ LiteLLM 통합 예제...")
    
    try:
        # LiteLLM 클라이언트 생성
        from litellm import completion
        
        # Opik으로 LiteLLM 추적
        opik_client = opik.Opik(
            project_name=os.getenv("OPIK_PROJECT_NAME", "Default Project")
        )
        
        # LiteLLM 완성 요청 (여러 제공업체 지원)
        response = completion(
            model="gpt-3.5-turbo",  # 또는 "claude-3-sonnet-20240229", "gemini-pro" 등
            messages=[
                {"role": "user", "content": "What is natural language processing?"}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        print(f"✅ LiteLLM 응답: {response.choices[0].message.content}")
        return True
        
    except ImportError:
        print("⚠️  LiteLLM 라이브러리가 설치되지 않았습니다.")
        print("   pip install litellm")
        return False
    except Exception as e:
        print(f"❌ LiteLLM 통합 실패: {e}")
        return False

def custom_llm_integration_example():
    """
    커스텀 LLM 통합 예제
    """
    print("\n🛠️  커스텀 LLM 통합 예제...")
    
    # Opik 클라이언트 생성
    opik_client = opik.Opik(
        project_name=os.getenv("OPIK_PROJECT_NAME", "Default Project")
    )
    
    # 커스텀 LLM 함수 정의
    def custom_llm_call(prompt: str, model: str = "custom-model") -> str:
        """
        커스텀 LLM 호출 함수
        """
        # 실제 환경에서는 여기서 LLM API를 호출합니다
        # 예시를 위해 간단한 응답 생성
        responses = {
            "what is ai": "Artificial Intelligence is the simulation of human intelligence in machines.",
            "what is ml": "Machine Learning is a subset of AI that enables computers to learn from data.",
            "what is nlp": "Natural Language Processing is a field of AI that focuses on the interaction between computers and human language."
        }
        
        prompt_lower = prompt.lower()
        for key, response in responses.items():
            if key in prompt_lower:
                return response
        
        return "I'm a custom AI model. I can help you with questions about AI, ML, and NLP."
    
    # @opik.track 데코레이터로 커스텀 함수 추적
    @opik.track
    def tracked_custom_llm(prompt: str) -> str:
        return custom_llm_call(prompt)
    
    # 추적된 함수 호출
    response = tracked_custom_llm("What is AI?")
    print(f"✅ 커스텀 LLM 응답: {response}")
    
    return True

def main():
    """메인 함수"""
    print("=" * 60)
    print("🎯 Opik Python SDK LLM 통합 예제")
    print("=" * 60)
    
    # 환경변수 확인
    print("🔍 환경변수 확인 중...")
    required_env_vars = [
        "OPIK_PROJECT_NAME"
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  다음 환경변수가 설정되지 않았습니다: {', '.join(missing_vars)}")
        print("   기본값을 사용하여 계속 진행합니다...")
    
    # 통합 예제 실행
    results = []
    
    # 1. OpenAI 통합
    results.append(("OpenAI", openai_integration_example()))
    
    # 2. Anthropic 통합
    results.append(("Anthropic", anthropic_integration_example()))
    
    # 3. LangChain 통합
    results.append(("LangChain", langchain_integration_example()))
    
    # 4. LiteLLM 통합
    results.append(("LiteLLM", litellm_integration_example()))
    
    # 5. 커스텀 LLM 통합
    results.append(("Custom LLM", custom_llm_integration_example()))
    
    # 결과 요약
    print("\n📊 통합 결과 요약:")
    successful = 0
    for name, success in results:
        status = "✅ 성공" if success else "❌ 실패"
        print(f"   - {name}: {status}")
        if success:
            successful += 1
    
    print(f"\n🎉 {successful}/{len(results)}개 통합이 성공했습니다!")
    
    if successful > 0:
        print("\n📊 Opik 웹 UI에서 결과를 확인하세요:")
        print("   http://localhost:5173")
    
    print("\n💡 추가 통합을 위해서는:")
    print("   1. 해당 LLM 제공업체의 API 키를 설정하세요")
    print("   2. 필요한 라이브러리를 설치하세요")
    print("   3. Opik 서버가 실행 중인지 확인하세요")

if __name__ == "__main__":
    main()
