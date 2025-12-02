"""다양한 질문 유형 테스트 시나리오"""
from typing import List, Dict, Any

# 테스트 시나리오 데이터
TEST_SCENARIOS: List[Dict[str, Any]] = [
    {
        "id": "test-001",
        "category": "인허가 절차",
        "question": "태양광 발전소 건설 시 필요한 인허가는?",
        "expected_keywords": ["태양광", "발전소", "인허가"],
        "expected_laws": ["law-001", "law-003", "law-004"],
        "description": "신재생에너지 발전사업 인허가 절차 질문"
    },
    {
        "id": "test-002",
        "category": "법령 해석",
        "question": "건축법 제11조의 건축허가 절차는?",
        "expected_keywords": ["건축법", "제11조", "건축허가"],
        "expected_laws": ["law-001"],
        "description": "특정 조문에 대한 질문"
    },
    {
        "id": "test-003",
        "category": "법령 관계",
        "question": "신재생에너지법과 전기사업법의 관계는?",
        "expected_keywords": ["신재생에너지법", "전기사업법", "관계"],
        "expected_laws": ["law-003", "law-004"],
        "description": "법령 간 관계 질문"
    },
    {
        "id": "test-004",
        "category": "환경 평가",
        "question": "태양광 발전소 건설 시 환경영향평가가 필요한가?",
        "expected_keywords": ["태양광", "발전소", "환경영향평가"],
        "expected_laws": ["law-005"],
        "description": "환경 평가 필요 여부 질문"
    },
    {
        "id": "test-005",
        "category": "지역별 질문",
        "question": "인천 서구에서 태양광 발전소 건설 시 필요한 절차는?",
        "expected_keywords": ["인천", "서구", "태양광", "발전소"],
        "expected_laws": ["law-001", "law-002", "law-003", "law-004"],
        "description": "지역 정보가 포함된 질문"
    },
    {
        "id": "test-006",
        "category": "정의 질문",
        "question": "건축물의 정의는 무엇인가?",
        "expected_keywords": ["건축물", "정의"],
        "expected_laws": ["law-001"],
        "description": "법률 용어 정의 질문"
    },
    {
        "id": "test-007",
        "category": "조건부 질문",
        "question": "발전용량이 1만킬로와트 이상인 경우 환경영향평가가 필요한가?",
        "expected_keywords": ["발전용량", "1만킬로와트", "환경영향평가"],
        "expected_laws": ["law-005"],
        "description": "조건이 포함된 질문"
    },
    {
        "id": "test-008",
        "category": "비교 질문",
        "question": "건축허가와 건축신고의 차이는?",
        "expected_keywords": ["건축허가", "건축신고", "차이"],
        "expected_laws": ["law-001"],
        "description": "비교 질문"
    },
    {
        "id": "test-009",
        "category": "복합 질문",
        "question": "산지에 태양광 발전소를 건설하려면 어떤 인허가가 필요한가?",
        "expected_keywords": ["산지", "태양광", "발전소", "인허가"],
        "expected_laws": ["law-001", "law-003", "law-004", "law-006"],
        "description": "여러 법령이 관련된 복합 질문"
    },
    {
        "id": "test-010",
        "category": "절차 질문",
        "question": "풍력 발전사업 인허가 절차는?",
        "expected_keywords": ["풍력", "발전사업", "인허가", "절차"],
        "expected_laws": ["law-001", "law-003", "law-004", "law-005"],
        "description": "절차에 대한 질문"
    }
]


def get_test_scenarios() -> List[Dict[str, Any]]:
    """모든 테스트 시나리오 반환"""
    return TEST_SCENARIOS


def get_scenarios_by_category(category: str) -> List[Dict[str, Any]]:
    """카테고리별 테스트 시나리오 반환"""
    return [s for s in TEST_SCENARIOS if s["category"] == category]


def get_scenario_by_id(scenario_id: str) -> Dict[str, Any] | None:
    """ID로 테스트 시나리오 조회"""
    for scenario in TEST_SCENARIOS:
        if scenario["id"] == scenario_id:
            return scenario
    return None

