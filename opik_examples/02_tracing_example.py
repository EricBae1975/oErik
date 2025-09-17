#!/usr/bin/env python3
"""
Opik Python SDK 트레이싱 예제

이 예제는 Opik SDK를 사용하여 LLM 호출을 추적하는 방법을 보여줍니다.
"""

import opik
import os
import time
from typing import Dict, Any

def create_simple_trace(client: opik.Opik) -> str:
    """
    간단한 트레이스를 생성합니다.
    """
    print("📝 간단한 트레이스 생성 중...")
    
    # 트레이스 생성
    trace = client.trace(
        name="simple_llm_call",
        input={"query": "What is artificial intelligence?"},
        output={"answer": "Artificial Intelligence (AI) is a branch of computer science..."},
        metadata={
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 150
        },
        tags=["demo", "ai", "education"]
    )
    
    print(f"✅ 트레이스 생성 완료! ID: {trace.id}")
    return trace.id

def create_trace_with_spans(client: opik.Opik) -> str:
    """
    스팬이 포함된 복잡한 트레이스를 생성합니다.
    """
    print("\n🔗 스팬이 포함된 트레이스 생성 중...")
    
    # 메인 트레이스 생성
    trace = client.trace(
        name="complex_ai_pipeline",
        input={"user_query": "Explain quantum computing"},
        tags=["demo", "quantum", "complex"]
    )
    
    # 첫 번째 스팬: 쿼리 전처리
    span1 = trace.span(
        name="query_preprocessing",
        input={"raw_query": "Explain quantum computing"},
        output={"processed_query": "Explain quantum computing in simple terms"},
        metadata={"step": "preprocessing", "language": "en"}
    )
    
    # 두 번째 스팬: LLM 호출
    span2 = trace.span(
        name="llm_generation",
        input={"prompt": "Explain quantum computing in simple terms"},
        output={"response": "Quantum computing uses quantum mechanical phenomena..."},
        metadata={
            "model": "gpt-4",
            "temperature": 0.5,
            "tokens_used": 250
        }
    )
    
    # 세 번째 스팬: 응답 후처리
    span3 = trace.span(
        name="response_postprocessing",
        input={"raw_response": "Quantum computing uses quantum mechanical phenomena..."},
        output={"final_response": "Quantum computing is a revolutionary technology..."},
        metadata={"step": "postprocessing", "format": "user_friendly"}
    )
    
    # 트레이스 완료
    trace.end(
        output={"final_answer": "Quantum computing is a revolutionary technology..."},
        metadata={"total_tokens": 250, "processing_time": 2.5}
    )
    
    print(f"✅ 복잡한 트레이스 생성 완료! ID: {trace.id}")
    return trace.id

def create_trace_with_decorator():
    """
    @opik.track 데코레이터를 사용한 트레이싱 예제
    """
    print("\n🎯 @opik.track 데코레이터 사용 예제...")
    
    @opik.track
    def ai_chatbot(query: str) -> str:
        """
        AI 챗봇 함수 - 자동으로 트레이싱됩니다.
        """
        # 시뮬레이션된 AI 응답 생성
        time.sleep(0.5)  # 처리 시간 시뮬레이션
        
        if "weather" in query.lower():
            return "I can help you with weather information. Please provide your location."
        elif "time" in query.lower():
            return f"The current time is {time.strftime('%H:%M:%S')}"
        else:
            return "I'm an AI assistant. How can I help you today?"
    
    # 함수 호출 (자동으로 트레이싱됨)
    response = ai_chatbot("What's the weather like?")
    print(f"🤖 AI 응답: {response}")
    
    return "decorator_trace"

def search_traces(client: opik.Opik, trace_ids: list):
    """
    생성된 트레이스들을 검색합니다.
    """
    print("\n🔍 트레이스 검색 중...")
    
    try:
        # 최근 트레이스 검색
        traces = client.search_traces(
            max_results=10
        )
        
        print(f"✅ {len(traces)}개의 트레이스를 찾았습니다:")
        for i, trace in enumerate(traces, 1):
            print(f"   {i}. {trace.name} (ID: {trace.id[:8]}...)")
            
    except Exception as e:
        print(f"❌ 트레이스 검색 실패: {e}")

def main():
    """메인 함수"""
    print("=" * 60)
    print("🎯 Opik Python SDK 트레이싱 예제")
    print("=" * 60)
    
    # Opik 클라이언트 설정
    client = opik.Opik(
        project_name=os.getenv("OPIK_PROJECT_NAME", "Default Project")
    )
    
    trace_ids = []
    
    try:
        # 1. 간단한 트레이스 생성
        trace_id1 = create_simple_trace(client)
        trace_ids.append(trace_id1)
        
        # 2. 스팬이 포함된 복잡한 트레이스 생성
        trace_id2 = create_trace_with_spans(client)
        trace_ids.append(trace_id2)
        
        # 3. 데코레이터를 사용한 트레이싱
        trace_id3 = create_trace_with_decorator()
        trace_ids.append(trace_id3)
        
        # 4. 트레이스 검색
        search_traces(client, trace_ids)
        
        print("\n🎉 트레이싱 예제가 완료되었습니다!")
        print("\n📊 Opik 웹 UI에서 결과를 확인하세요:")
        print("   http://localhost:5173")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        print("\n💡 해결 방법:")
        print("   1. Opik 서버가 실행 중인지 확인하세요")
        print("   2. API 키가 올바른지 확인하세요")
        print("   3. 네트워크 연결을 확인하세요")

if __name__ == "__main__":
    main()
