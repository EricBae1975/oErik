#!/usr/bin/env python3
"""
Opik Python SDK 평가(Evaluation) 예제

이 예제는 Opik SDK를 사용하여 LLM 모델을 평가하는 방법을 보여줍니다.
"""

import opik
import os
from typing import List, Dict, Any

def create_dataset(client: opik.Opik) -> str:
    """
    평가용 데이터셋을 생성합니다.
    """
    print("📊 평가용 데이터셋 생성 중...")
    
    # 데이터셋 생성
    dataset = client.create_dataset(
        name="ai_qa_evaluation_dataset_v4",
        description="AI 질문-답변 평가를 위한 샘플 데이터셋"
    )
    
    # 데이터셋에 아이템 추가
    dataset_items = [
        {
            "input": {"question": "What is artificial intelligence?"},
            "expected_output": {"answer": "Artificial Intelligence (AI) is a branch of computer science that aims to create machines capable of intelligent behavior."}
        },
        {
            "input": {"question": "How does machine learning work?"},
            "expected_output": {"answer": "Machine learning is a subset of AI that enables computers to learn and improve from experience without being explicitly programmed."}
        },
        {
            "input": {"question": "What is the difference between AI and ML?"},
            "expected_output": {"answer": "AI is the broader concept of machines being able to carry out tasks in a smart way, while ML is a specific application of AI where machines learn from data."}
        },
        {
            "input": {"question": "What are neural networks?"},
            "expected_output": {"answer": "Neural networks are computing systems inspired by biological neural networks that can learn to perform tasks by analyzing training data."}
        },
        {
            "input": {"question": "What is deep learning?"},
            "expected_output": {"answer": "Deep learning is a subset of machine learning that uses neural networks with multiple layers to model and understand complex patterns in data."}
        }
    ]
    
    dataset.insert(dataset_items)
    
    print(f"✅ 데이터셋 생성 완료! 이름: {dataset.name}")
    print(f"   - 아이템 수: {len(dataset_items)}")
    
    return dataset.name

def create_experiment(client: opik.Opik, dataset_name: str) -> str:
    """
    평가 실험을 생성합니다.
    """
    print("\n🧪 평가 실험 생성 중...")
    
    # 실험 생성
    experiment = client.create_experiment(
        name="ai_qa_model_evaluation",
        dataset_name=dataset_name
    )
    
    print(f"✅ 실험 생성 완료! 이름: {experiment.name}")
    return experiment.name

def define_evaluation_metrics():
    """
    평가 메트릭을 정의합니다.
    """
    print("\n📏 평가 메트릭 정의 중...")
    
    # 간단한 정확도 메트릭 정의
    def accuracy_metric(input_data: Dict[str, Any], output_data: Dict[str, Any], expected_output: Dict[str, Any]) -> float:
        """
        정확도 메트릭: 예상 답변과 실제 답변의 유사도를 측정
        """
        expected = expected_output.get("answer", "").lower()
        actual = output_data.get("answer", "").lower()
        
        # 간단한 키워드 기반 정확도 계산
        expected_words = set(expected.split())
        actual_words = set(actual.split())
        
        if not expected_words:
            return 0.0
        
        intersection = expected_words.intersection(actual_words)
        accuracy = len(intersection) / len(expected_words)
        
        return min(accuracy, 1.0)
    
    # 응답 길이 메트릭 정의
    def response_length_metric(input_data: Dict[str, Any], output_data: Dict[str, Any], expected_output: Dict[str, Any]) -> float:
        """
        응답 길이 메트릭: 응답의 적절한 길이를 측정
        """
        actual = output_data.get("answer", "")
        expected = expected_output.get("answer", "")
        
        actual_length = len(actual)
        expected_length = len(expected)
        
        if expected_length == 0:
            return 0.0
        
        # 길이 차이의 비율 (0에 가까울수록 좋음)
        length_ratio = abs(actual_length - expected_length) / expected_length
        return max(0.0, 1.0 - length_ratio)
    
    print("✅ 평가 메트릭 정의 완료!")
    print("   - 정확도 메트릭: 키워드 기반 유사도 측정")
    print("   - 응답 길이 메트릭: 적절한 길이 측정")
    
    return {
        "accuracy": accuracy_metric,
        "response_length": response_length_metric
    }

def simulate_llm_model(question: str) -> str:
    """
    시뮬레이션된 LLM 모델
    실제 환경에서는 실제 LLM API를 호출합니다.
    """
    # 간단한 시뮬레이션된 응답 생성
    responses = {
        "what is artificial intelligence": "Artificial Intelligence (AI) is a branch of computer science that aims to create machines capable of intelligent behavior and decision-making.",
        "how does machine learning work": "Machine learning is a subset of AI that enables computers to learn and improve from experience without being explicitly programmed for every task.",
        "what is the difference between ai and ml": "AI is the broader concept of machines being able to carry out tasks in a smart way, while ML is a specific application of AI where machines learn from data.",
        "what are neural networks": "Neural networks are computing systems inspired by biological neural networks that can learn to perform tasks by analyzing training data and identifying patterns.",
        "what is deep learning": "Deep learning is a subset of machine learning that uses neural networks with multiple layers to model and understand complex patterns in data."
    }
    
    question_lower = question.lower()
    for key, response in responses.items():
        if key in question_lower:
            return response
    
    return "I'm an AI assistant. I can help you with questions about artificial intelligence, machine learning, and related topics."

def run_evaluation(client: opik.Opik, dataset_name: str, experiment_name: str):
    """
    평가를 실행합니다.
    """
    print("\n🚀 평가 실행 중...")
    
    # 데이터셋 로드
    dataset = client.get_dataset(dataset_name)
    dataset_items = dataset.get_items()
    
    # 평가 메트릭 정의
    metrics = define_evaluation_metrics()
    
    # 평가 결과 저장
    evaluation_results = []
    
    print(f"📝 {len(dataset_items)}개 아이템 평가 중...")
    
    for i, item in enumerate(dataset_items, 1):
        question = item["input"]["question"]
        expected_answer = item["expected_output"]["answer"]
        
        print(f"   {i}. 질문: {question}")
        
        # LLM 모델 시뮬레이션
        actual_answer = simulate_llm_model(question)
        
        # 메트릭 계산
        accuracy_score = metrics["accuracy"](
            item["input"], 
            {"answer": actual_answer}, 
            item["expected_output"]
        )
        
        length_score = metrics["response_length"](
            item["input"], 
            {"answer": actual_answer}, 
            item["expected_output"]
        )
        
        # 결과 저장
        result = {
            "question": question,
            "expected_answer": expected_answer,
            "actual_answer": actual_answer,
            "accuracy_score": accuracy_score,
            "length_score": length_score,
            "overall_score": (accuracy_score + length_score) / 2
        }
        
        evaluation_results.append(result)
        
        print(f"      정확도: {accuracy_score:.2f}, 길이점수: {length_score:.2f}, 전체점수: {result['overall_score']:.2f}")
    
    # 전체 결과 요약
    avg_accuracy = sum(r["accuracy_score"] for r in evaluation_results) / len(evaluation_results)
    avg_length = sum(r["length_score"] for r in evaluation_results) / len(evaluation_results)
    avg_overall = sum(r["overall_score"] for r in evaluation_results) / len(evaluation_results)
    
    print(f"\n📊 평가 결과 요약:")
    print(f"   - 평균 정확도: {avg_accuracy:.2f}")
    print(f"   - 평균 길이점수: {avg_length:.2f}")
    print(f"   - 평균 전체점수: {avg_overall:.2f}")
    
    return evaluation_results

def main():
    """메인 함수"""
    print("=" * 60)
    print("🎯 Opik Python SDK 평가(Evaluation) 예제")
    print("=" * 60)
    
    # Opik 클라이언트 설정
    client = opik.Opik(
        project_name=os.getenv("OPIK_PROJECT_NAME", "Default Project")
    )
    
    try:
        # 1. 데이터셋 생성
        dataset_name = create_dataset(client)
        
        # 2. 실험 생성
        experiment_name = create_experiment(client, dataset_name)
        
        # 3. 평가 실행
        results = run_evaluation(client, dataset_name, experiment_name)
        
        print("\n🎉 평가 예제가 완료되었습니다!")
        print("\n📊 Opik 웹 UI에서 결과를 확인하세요:")
        print("   http://localhost:5173")
        print(f"   - 데이터셋: {dataset_name}")
        print(f"   - 실험: {experiment_name}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        print("\n💡 해결 방법:")
        print("   1. Opik 서버가 실행 중인지 확인하세요")
        print("   2. API 키가 올바른지 확인하세요")
        print("   3. 네트워크 연결을 확인하세요")

if __name__ == "__main__":
    main()
