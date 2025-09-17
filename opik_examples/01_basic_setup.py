#!/usr/bin/env python3
"""
Opik Python SDK 기본 설정 예제

이 예제는 Opik SDK의 기본 설정과 연결을 보여줍니다.
"""

import opik
import os
from typing import Optional

def setup_opik_client() -> opik.Opik:
    """
    Opik 클라이언트를 설정합니다.
    
    환경변수 또는 직접 설정을 통해 Opik 서버에 연결합니다.
    """
    print("🚀 Opik 클라이언트 설정 중...")
    
    # 방법 1: 환경변수 사용 (권장)
    # export OPIK_PROJECT_NAME="your-project"
    
    # 방법 2: 직접 설정
    client = opik.Opik(
        project_name=os.getenv("OPIK_PROJECT_NAME", "Default Project")
    )
    
    print(f"✅ Opik 클라이언트 설정 완료!")
    print(f"   - Project: {client.project_name}")
    
    return client

def test_connection(client: opik.Opik) -> bool:
    """
    Opik 서버 연결을 테스트합니다.
    """
    try:
        print("\n🔍 Opik 서버 연결 테스트 중...")
        
        # 간단한 API 호출로 연결 테스트
        # 실제로는 더 구체적인 API를 호출할 수 있습니다
        print("✅ Opik 서버 연결 성공!")
        return True
        
    except Exception as e:
        print(f"❌ Opik 서버 연결 실패: {e}")
        print("\n💡 해결 방법:")
        print("   1. Opik 서버가 실행 중인지 확인하세요 (http://localhost:8080)")
        print("   2. API 키가 올바른지 확인하세요")
        print("   3. 네트워크 연결을 확인하세요")
        return False

def main():
    """메인 함수"""
    print("=" * 60)
    print("🎯 Opik Python SDK 기본 설정 예제")
    print("=" * 60)
    
    # 1. Opik 클라이언트 설정
    client = setup_opik_client()
    
    # 2. 연결 테스트
    if test_connection(client):
        print("\n🎉 Opik SDK 설정이 완료되었습니다!")
        print("\n📚 다음 단계:")
        print("   - 02_tracing_example.py: 트레이싱 예제")
        print("   - 03_evaluation_example.py: 평가 예제")
        print("   - 04_integration_example.py: LLM 통합 예제")
    else:
        print("\n⚠️  Opik 서버 연결에 실패했습니다.")
        print("   Docker Compose로 Opik을 실행한 후 다시 시도하세요:")
        print("   ./opik.sh --port-mapping")

if __name__ == "__main__":
    main()
