# 목업 데이터 준비 가이드

## 개요

법령 Q&A 웹앱 개발 초기 단계에서 실제 국가법령정보센터 API를 사용하기 전까지, 개발 및 테스트를 위한 목업 데이터를 준비합니다.

## 목업 데이터 구조

### 법령 데이터 모델

```python
from typing import List, Optional
from pydantic import BaseModel

class Subparagraph(BaseModel):
    """항/호/목"""
    id: str
    article_id: str
    type: str  # "항", "호", "목"
    number: str  # "1", "가", "①"
    content: str

class Article(BaseModel):
    """조문"""
    id: str
    law_id: str
    number: str  # "제1조"
    title: Optional[str] = None
    content: str
    subparagraphs: List[Subparagraph] = []
    related_articles: List[str] = []  # 관련 조문 ID 목록

class Law(BaseModel):
    """법령"""
    id: str
    name: str  # 법령명
    type: str  # "법률", "시행령", "시행규칙", "조례" 등
    enactment_date: str  # 제정일 (YYYY-MM-DD)
    amendment_date: str  # 최신 개정일 (YYYY-MM-DD)
    category: List[str]  # ["건설", "건축", "에너지", "환경"] 등
    articles: List[Article] = []
```

## 목업 데이터 범위

### 최우선 법령 (인허가 관련)

1. **건축법** (`law-001`)
   - 건축물의 대지·구조·설비 기준
   - 건축 인허가 절차 관련 조문
   - 주요 조문: 제1조(목적), 제2조(정의), 제11조(건축허가), 제14조(건축신고)

2. **도시계획법** (`law-002`)
   - 도시계획의 수립 및 변경
   - 개발행위 허가 관련 조문
   - 주요 조문: 제1조(목적), 제2조(정의), 제56조(개발행위의 허가)

3. **전기사업법** (`law-003`)
   - 전기사업의 허가 및 신고
   - 발전사업 관련 조문
   - 주요 조문: 제1조(목적), 제7조(전기사업의 허가), 제8조(발전사업의 신고)

4. **신에너지 및 재생에너지 개발·이용·보급 촉진법** (`law-004`)
   - 신재생에너지 개발 지원
   - 태양광, 풍력 등 발전사업 관련 조문
   - 주요 조문: 제1조(목적), 제2조(정의), 제12조(신재생에너지 발전사업)

5. **환경영향평가법** (`law-005`)
   - 환경영향평가 실시 의무
   - 사전환경성검토 관련 조문
   - 주요 조문: 제1조(목적), 제4조(환경영향평가 대상사업)

6. **산지관리법** (`law-006`)
   - 산지 전용 허가 및 신고
   - 산지 개발 관련 조문
   - 주요 조문: 제1조(목적), 제14조(산지전용허가)

### 지역 조례 데이터

- 광역시·도별 도시계획 조례
- 시·군·구별 건축 조례
- 지역별 신재생에너지 관련 조례

### 인허가 절차 데이터

- 태양광 발전사업 인허가 절차
- 풍력 발전사업 인허가 절차
- 건축 인허가 절차

### 법령 Q&A 시나리오 데이터

실제 사용자 질문과 답변 예시:
- "인천 서구에서 태양광 발전소 건설 시 필요한 인허가는?"
- "건축법 제11조의 건축허가 절차는?"
- "신재생에너지법과 전기사업법의 관계는?"

## 목업 데이터 생성 방법

### 1. 데이터 파일 구조

```
backend/app/mock/
├── __init__.py
├── law_data.py          # 법령 목업 데이터
├── procedure_data.py     # 인허가 절차 데이터
└── qa_scenarios.py      # Q&A 시나리오 데이터
```

### 2. 법령 데이터 예시

```python
# backend/app/mock/law_data.py

MOCK_LAWS = [
    {
        "id": "law-001",
        "name": "건축법",
        "type": "법률",
        "enactment_date": "1962-01-20",
        "amendment_date": "2023-06-11",
        "category": ["건설", "건축"],
        "articles": [
            {
                "id": "art-001-001",
                "law_id": "law-001",
                "number": "제1조",
                "title": "목적",
                "content": "이 법은 건축물의 대지·구조·설비 기준 및 용도 등을 정하여 건축물의 안전·기능·환경 및 미관을 향상시킴으로써 공공복리의 증진에 이바지하는 것을 목적으로 한다.",
                "subparagraphs": [],
                "related_articles": []
            },
            {
                "id": "art-001-011",
                "law_id": "law-001",
                "number": "제11조",
                "title": "건축허가",
                "content": "건축물을 건축하려는 자는 특별시장·광역시장·특별자치시장·도지사·특별자치도지사 또는 시장·군수·구청장(이하 "행정기관의 장"이라 한다)의 허가를 받아야 한다.",
                "subparagraphs": [
                    {
                        "id": "subp-001-011-001",
                        "article_id": "art-001-011",
                        "type": "항",
                        "number": "1",
                        "content": "대지면적이 200제곱미터 이상인 건축물"
                    }
                ],
                "related_articles": ["art-001-014"]
            }
        ]
    }
]
```

### 3. 인허가 절차 데이터 예시

```python
# backend/app/mock/procedure_data.py

MOCK_PROCEDURES = [
    {
        "id": "proc-001",
        "title": "태양광 발전사업 인허가 절차",
        "category": ["에너지", "신재생에너지"],
        "steps": [
            {
                "step": 1,
                "title": "사전 협의",
                "description": "지역별 담당기관과 사전 협의",
                "required_documents": ["사업계획서", "부지확보 증명서류"],
                "duration": "1-2주",
                "authority": "시·군·구청"
            },
            {
                "step": 2,
                "title": "전기사업 신고",
                "description": "전기사업법에 따른 발전사업 신고",
                "required_documents": ["발전사업 신고서", "전기설비 공사계획서"],
                "duration": "2-3주",
                "authority": "산업통상자원부"
            }
        ],
        "related_laws": ["law-003", "law-004"]
    }
]
```

## 목업 데이터 사용 방법

### 1. 서비스 레이어에서 사용

```python
# backend/app/services/law_service.py

from app.mock.law_data import MOCK_LAWS

def search_laws(keyword: str) -> List[Law]:
    """키워드로 법령 검색 (목업 데이터 사용)"""
    results = []
    for law in MOCK_LAWS:
        # 키워드 매칭 로직
        if keyword.lower() in law["name"].lower():
            results.append(law)
    return results
```

### 2. API 엔드포인트에서 사용

```python
# backend/app/api/law.py

from app.mock.law_data import MOCK_LAWS

@router.get("/search")
async def search_laws(keyword: str):
    """법령 검색 API (목업 데이터)"""
    return {"laws": MOCK_LAWS}
```

## 실제 API 전환 시 주의사항

1. **데이터 구조 일치**: 목업 데이터 구조를 실제 국가법령정보센터 API 응답 구조와 일치시켜야 함
2. **ID 체계**: 실제 API의 법령 ID 체계를 고려하여 목업 데이터 ID 설계
3. **데이터 검증**: 실제 API 전환 시 Pydantic 스키마로 데이터 검증 필요
4. **점진적 전환**: 목업 데이터와 실제 API를 병행하여 점진적으로 전환

## 데이터 업데이트

- 법령 개정사항 반영: `amendment_date` 필드 업데이트
- 새로운 법령 추가: 목업 데이터 배열에 추가
- 조문 내용 수정: 실제 법령 개정사항 반영

## 참고 자료

- 국가법령정보센터 API 문서
- 각 법령의 공식 조문
- 인허가 절차 관련 행정규칙


