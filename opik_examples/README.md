# Opik Python SDK 사용 예제

이 디렉토리는 Opik Python SDK의 다양한 사용 예제를 포함합니다.

## 📋 예제 목록

### 0. 간단한 테스트 (`00_simple_test.py`)
- Opik SDK 기본 연결 테스트
- 간단한 트레이스 생성
- @opik.track 데코레이터 테스트

### 1. 기본 설정 (`01_basic_setup.py`)
- Opik 클라이언트 설정
- 서버 연결 테스트
- 기본 구성 확인

### 2. 트레이싱 (`02_tracing_example.py`)
- 간단한 트레이스 생성
- 스팬이 포함된 복잡한 트레이스
- `@opik.track` 데코레이터 사용
- 트레이스 검색

### 3. 평가 (`03_evaluation_example.py`)
- 데이터셋 생성 및 관리
- 실험 생성
- 커스텀 평가 메트릭 정의
- LLM 모델 평가 실행

### 4. LLM 통합 (`04_integration_example.py`)
- OpenAI 통합
- Anthropic 통합
- LangChain 통합
- LiteLLM 통합
- 커스텀 LLM 통합

## 🚀 시작하기

### 1. 환경 설정

```bash
# 가상환경 생성 및 활성화
python3 -m venv opik_examples_env
source opik_examples_env/bin/activate

# Opik SDK 설치
pip install opik
```

### 2. Opik 서버 실행

```bash
# Opik Docker Compose 실행
./opik.sh --port-mapping
```

### 3. 환경변수 설정 (선택사항)

```bash
export OPIK_PROJECT_NAME="Default Project"

# LLM 통합을 위한 API 키들
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

### 4. 예제 실행

```bash
# 간단한 테스트 예제 (권장)
python 00_simple_test.py

# 기본 설정 예제
python 01_basic_setup.py

# 트레이싱 예제
python 02_tracing_example.py

# 평가 예제
python 03_evaluation_example.py

# LLM 통합 예제
python 04_integration_example.py
```

## 📊 결과 확인

예제 실행 후 Opik 웹 UI에서 결과를 확인할 수 있습니다:

- **웹 UI**: http://localhost:5173
- **API 문서**: http://localhost:8080

## 🔧 문제 해결

### 일반적인 문제들

1. **연결 실패**
   - Opik 서버가 실행 중인지 확인
   - API 키가 올바른지 확인
   - 네트워크 연결 확인

2. **라이브러리 누락**
   - 필요한 라이브러리 설치
   - 가상환경 활성화 확인

3. **API 키 오류**
   - 환경변수 설정 확인
   - LLM 제공업체 API 키 유효성 확인

### 도움말

- [Opik 공식 문서](https://docs.opik.com)
- [Python SDK 문서](https://docs.opik.com/python-sdk)
- [GitHub 저장소](https://github.com/opik-ai/opik)

## 📝 라이센스

이 예제들은 Apache License 2.0 하에 제공됩니다.
