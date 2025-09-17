#!/usr/bin/env python3
"""
Opik Python SDK 간단한 테스트 예제

이 예제는 Opik SDK의 기본 기능을 테스트합니다.
"""

import opik
import os

def test_basic_connection():
    """기본 연결 테스트"""
    print("🔗 Opik 서버 연결 테스트...")
    
    try:
        # Opik 클라이언트 생성 (기본 설정)
        client = opik.Opik()
        
        print(f"✅ Opik 클라이언트 생성 성공!")
        print(f"   - Project: {client.project_name}")
        
        # 간단한 트레이스 생성 테스트
        print("\n📝 간단한 트레이스 생성 테스트...")
        
        trace = client.trace(
            name="test_trace",
            input={"message": "Hello Opik!"},
            output={"response": "Hello from Opik!"},
            metadata={"test": True}
        )
        
        print(f"✅ 트레이스 생성 성공! ID: {trace.id}")
        
        # 데이터 플러시 (서버로 전송)
        print("\n💾 데이터 플러시 중...")
        opik.flush_tracker()
        print("✅ 데이터 플러시 완료!")
        
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

def test_track_decorator():
    """@opik.track 데코레이터 테스트"""
    print("\n🎯 @opik.track 데코레이터 테스트...")
    
    @opik.track
    def simple_function(input_text: str) -> str:
        """간단한 함수를 추적합니다."""
        return f"Processed: {input_text}"
    
    try:
        result = simple_function("Hello World!")
        print(f"✅ 함수 실행 성공: {result}")
        
        # 데이터 플러시
        opik.flush_tracker()
        print("✅ 추적 데이터 플러시 완료!")
        
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

def main():
    """메인 함수"""
    print("🚀 Opik Python SDK 간단한 테스트 시작\n")
    
    # 기본 연결 테스트
    connection_ok = test_basic_connection()
    
    # 데코레이터 테스트
    decorator_ok = test_track_decorator()
    
    # 결과 요약
    print("\n📊 테스트 결과 요약:")
    print(f"   - 기본 연결: {'✅ 성공' if connection_ok else '❌ 실패'}")
    print(f"   - 데코레이터: {'✅ 성공' if decorator_ok else '❌ 실패'}")
    
    if connection_ok and decorator_ok:
        print("\n🎉 모든 테스트 통과! Opik SDK가 정상적으로 작동합니다.")
    else:
        print("\n⚠️  일부 테스트가 실패했습니다. 설정을 확인해주세요.")

if __name__ == "__main__":
    main()
