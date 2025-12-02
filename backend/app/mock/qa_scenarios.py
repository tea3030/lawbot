"""법령 Q&A 시나리오 목업 데이터"""
from typing import List, Dict, Any

QAScenario = Dict[str, Any]

MOCK_QA_SCENARIOS: List[QAScenario] = [
    {
        "id": "qa-001",
        "question": "인천 서구에서 태양광 발전소 건설 시 필요한 인허가는?",
        "category": ["인허가", "태양광", "지역별"],
        "keywords": ["인천", "서구", "태양광", "발전소", "인허가"],
        "expected_answer_summary": "태양광 발전소 건설을 위해서는 건축허가, 전기사업 신고, 환경영향평가, 산지전용허가(해당 시) 등이 필요합니다.",
        "related_laws": ["law-001", "law-003", "law-004", "law-005", "law-006"],
        "related_procedures": ["proc-001"]
    },
    {
        "id": "qa-002",
        "question": "건축법 제11조의 건축허가 절차는?",
        "category": ["법령해석", "건축법"],
        "keywords": ["건축법", "제11조", "건축허가", "절차"],
        "expected_answer_summary": "건축법 제11조에 따르면 건축물을 건축하려는 자는 행정기관의 장의 허가를 받아야 합니다. 다만, 대지면적 200제곱미터 미만 등 일정 조건에 해당하는 경우 신고로 할 수 있습니다.",
        "related_laws": ["law-001"],
        "related_procedures": ["proc-003"]
    },
    {
        "id": "qa-003",
        "question": "신재생에너지법과 전기사업법의 관계는?",
        "category": ["법령관계", "에너지"],
        "keywords": ["신재생에너지법", "전기사업법", "관계"],
        "expected_answer_summary": "신재생에너지법 제12조에 따르면 신재생에너지를 이용한 발전사업을 하려는 자는 전기사업법 제7조 및 제8조에 따라 허가를 받거나 신고를 하여야 합니다. 즉, 신재생에너지법은 전기사업법의 특별법적 성격을 가집니다.",
        "related_laws": ["law-003", "law-004"],
        "related_procedures": ["proc-001", "proc-002"]
    },
    {
        "id": "qa-004",
        "question": "태양광 발전소 건설 시 환경영향평가가 필요한가?",
        "category": ["환경", "태양광"],
        "keywords": ["태양광", "발전소", "환경영향평가"],
        "expected_answer_summary": "환경영향평가법 제4조에 따르면 발전용량이 1만킬로와트 이상인 발전소 건설사업은 환경영향평가 대상사업입니다. 따라서 태양광 발전소도 발전용량에 따라 환경영향평가가 필요할 수 있습니다.",
        "related_laws": ["law-005"],
        "related_procedures": ["proc-001"]
    },
    {
        "id": "qa-005",
        "question": "농지에 태양광 설치 시 농지법과 전기사업법 중 어느 것이 우선 적용되나?",
        "category": ["법령충돌", "농지", "태양광"],
        "keywords": ["농지", "태양광", "농지법", "전기사업법", "우선순위"],
        "expected_answer_summary": "농지에 태양광을 설치하는 경우 농지법과 전기사업법이 모두 적용됩니다. 농지법에 따른 농지전용허가와 전기사업법에 따른 발전사업 신고가 모두 필요하며, 각 법령의 요건을 모두 충족해야 합니다.",
        "related_laws": ["law-003"],
        "related_procedures": ["proc-001"]
    },
    {
        "id": "qa-006",
        "question": "풍력 발전사업 인허가 절차는?",
        "category": ["인허가", "풍력"],
        "keywords": ["풍력", "발전사업", "인허가", "절차"],
        "expected_answer_summary": "풍력 발전사업을 위해서는 사전 협의, 전기사업 신고, 환경영향평가 등의 절차가 필요합니다. 총 소요기간은 약 6-9개월입니다.",
        "related_laws": ["law-001", "law-003", "law-004", "law-005"],
        "related_procedures": ["proc-002"]
    }
]


def get_all_scenarios() -> List[QAScenario]:
    """모든 Q&A 시나리오 반환"""
    return MOCK_QA_SCENARIOS


def get_scenario_by_id(scenario_id: str) -> QAScenario | None:
    """시나리오 ID로 시나리오 조회"""
    for scenario in MOCK_QA_SCENARIOS:
        if scenario["id"] == scenario_id:
            return scenario
    return None


def search_scenarios_by_keyword(keyword: str) -> List[QAScenario]:
    """키워드로 시나리오 검색"""
    keyword_lower = keyword.lower()
    results = []
    
    for scenario in MOCK_QA_SCENARIOS:
        if keyword_lower in scenario["question"].lower():
            results.append(scenario)
            continue
        
        if any(keyword_lower in kw.lower() for kw in scenario.get("keywords", [])):
            results.append(scenario)
            continue
        
        if any(keyword_lower in cat.lower() for cat in scenario.get("category", [])):
            results.append(scenario)
    
    return results

