"""인허가 절차 목업 데이터"""
from typing import List, Dict, Any

ProcedureData = Dict[str, Any]

MOCK_PROCEDURES: List[ProcedureData] = [
    {
        "id": "proc-001",
        "title": "태양광 발전사업 인허가 절차",
        "category": ["에너지", "신재생에너지", "태양광"],
        "description": "태양광 발전소 건설을 위한 인허가 절차",
        "steps": [
            {
                "step": 1,
                "title": "사전 협의",
                "description": "지역별 담당기관과 사전 협의",
                "required_documents": [
                    "사업계획서",
                    "부지확보 증명서류",
                    "위치도 및 배치도"
                ],
                "duration": "1-2주",
                "authority": "시·군·구청 건축과",
                "related_laws": ["law-001", "law-002"]
            },
            {
                "step": 2,
                "title": "건축허가 또는 신고",
                "description": "건축법에 따른 건축허가 또는 신고",
                "required_documents": [
                    "건축허가(신고)서",
                    "건축물대장",
                    "구조계산서",
                    "설비계획서"
                ],
                "duration": "2-3주",
                "authority": "시·군·구청 건축과",
                "related_laws": ["law-001"]
            },
            {
                "step": 3,
                "title": "전기사업 신고",
                "description": "전기사업법에 따른 발전사업 신고",
                "required_documents": [
                    "발전사업 신고서",
                    "전기설비 공사계획서",
                    "전기설비 안전관리계획서"
                ],
                "duration": "2-3주",
                "authority": "산업통상자원부",
                "related_laws": ["law-003"]
            },
            {
                "step": 4,
                "title": "환경영향평가",
                "description": "환경영향평가법에 따른 환경영향평가 실시",
                "required_documents": [
                    "환경영향평가서",
                    "환경영향평가 협의신청서"
                ],
                "duration": "3-6개월",
                "authority": "환경부",
                "related_laws": ["law-005"],
                "condition": "발전용량 1만킬로와트 이상인 경우"
            },
            {
                "step": 5,
                "title": "산지전용허가",
                "description": "산지관리법에 따른 산지전용허가 (해당 시)",
                "required_documents": [
                    "산지전용허가신청서",
                    "산지전용 타당성 검토서"
                ],
                "duration": "2-4주",
                "authority": "산림청",
                "related_laws": ["law-006"],
                "condition": "산지에 건설하는 경우"
            }
        ],
        "related_laws": ["law-001", "law-002", "law-003", "law-004", "law-005", "law-006"],
        "total_duration": "6-9개월",
        "estimated_cost": "사업 규모에 따라 상이"
    },
    {
        "id": "proc-002",
        "title": "풍력 발전사업 인허가 절차",
        "category": ["에너지", "신재생에너지", "풍력"],
        "description": "풍력 발전소 건설을 위한 인허가 절차",
        "steps": [
            {
                "step": 1,
                "title": "사전 협의",
                "description": "지역별 담당기관과 사전 협의",
                "required_documents": [
                    "사업계획서",
                    "부지확보 증명서류",
                    "풍력자원 조사보고서"
                ],
                "duration": "1-2주",
                "authority": "시·군·구청",
                "related_laws": ["law-001", "law-002"]
            },
            {
                "step": 2,
                "title": "전기사업 신고",
                "description": "전기사업법에 따른 발전사업 신고",
                "required_documents": [
                    "발전사업 신고서",
                    "전기설비 공사계획서"
                ],
                "duration": "2-3주",
                "authority": "산업통상자원부",
                "related_laws": ["law-003"]
            },
            {
                "step": 3,
                "title": "환경영향평가",
                "description": "환경영향평가법에 따른 환경영향평가 실시",
                "required_documents": [
                    "환경영향평가서"
                ],
                "duration": "3-6개월",
                "authority": "환경부",
                "related_laws": ["law-005"]
            }
        ],
        "related_laws": ["law-001", "law-003", "law-004", "law-005"],
        "total_duration": "6-9개월",
        "estimated_cost": "사업 규모에 따라 상이"
    },
    {
        "id": "proc-003",
        "title": "건축 인허가 절차",
        "category": ["건축", "건설"],
        "description": "일반 건축물 건축을 위한 인허가 절차",
        "steps": [
            {
                "step": 1,
                "title": "건축허가 신청",
                "description": "건축법에 따른 건축허가 신청",
                "required_documents": [
                    "건축허가신청서",
                    "건축물대장",
                    "구조계산서",
                    "설비계획서",
                    "부지도 및 위치도"
                ],
                "duration": "2-3주",
                "authority": "시·군·구청 건축과",
                "related_laws": ["law-001"]
            },
            {
                "step": 2,
                "title": "도시계획 관련 허가",
                "description": "도시계획법에 따른 개발행위 허가 (해당 시)",
                "required_documents": [
                    "개발행위 허가신청서",
                    "개발계획서"
                ],
                "duration": "2-3주",
                "authority": "시·군·구청 도시계획과",
                "related_laws": ["law-002"],
                "condition": "도시계획시설부지 또는 개발제한구역인 경우"
            }
        ],
        "related_laws": ["law-001", "law-002"],
        "total_duration": "1-2개월",
        "estimated_cost": "건축물 규모에 따라 상이"
    }
]


def get_all_procedures() -> List[ProcedureData]:
    """모든 인허가 절차 데이터 반환"""
    return MOCK_PROCEDURES


def get_procedure_by_id(procedure_id: str) -> ProcedureData | None:
    """절차 ID로 절차 데이터 조회"""
    for procedure in MOCK_PROCEDURES:
        if procedure["id"] == procedure_id:
            return procedure
    return None


def search_procedures_by_keyword(keyword: str) -> List[ProcedureData]:
    """키워드로 절차 검색"""
    keyword_lower = keyword.lower()
    results = []
    
    for procedure in MOCK_PROCEDURES:
        if keyword_lower in procedure["title"].lower():
            results.append(procedure)
            continue
        
        if any(keyword_lower in cat.lower() for cat in procedure.get("category", [])):
            results.append(procedure)
            continue
        
        if keyword_lower in procedure.get("description", "").lower():
            results.append(procedure)
    
    return results

