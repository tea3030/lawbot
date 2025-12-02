"""법령 목업 데이터"""
from typing import List, Dict, Any

# 법령 데이터 타입 정의
LawData = Dict[str, Any]

MOCK_LAWS: List[LawData] = [
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
                "id": "art-001-002",
                "law_id": "law-001",
                "number": "제2조",
                "title": "정의",
                "content": "이 법에서 사용하는 용어의 뜻은 다음과 같다.",
                "subparagraphs": [
                    {
                        "id": "subp-001-002-001",
                        "article_id": "art-001-002",
                        "type": "항",
                        "number": "1",
                        "content": "\"건축물\"이란 토지에 정착하는 공작물 중 지붕과 기둥 또는 벽이 있는 것과 이에 딸린 시설물을 말한다."
                    },
                    {
                        "id": "subp-001-002-002",
                        "article_id": "art-001-002",
                        "type": "항",
                        "number": "2",
                        "content": "\"건축물의 용도\"란 건축물의 종류를 유사한 구조, 이용 목적 및 형태별로 묶어 분류한 것을 말한다."
                    }
                ],
                "related_articles": ["art-001-003"]
            },
            {
                "id": "art-001-011",
                "law_id": "law-001",
                "number": "제11조",
                "title": "건축허가",
                "content": "건축물을 건축하려는 자는 특별시장·광역시장·특별자치시장·도지사·특별자치도지사 또는 시장·군수·구청장(이하 \"행정기관의 장\"이라 한다)의 허가를 받아야 한다. 다만, 다음 각 호의 어느 하나에 해당하는 경우에는 그러하지 아니하다.",
                "subparagraphs": [
                    {
                        "id": "subp-001-011-001",
                        "article_id": "art-001-011",
                        "type": "호",
                        "number": "1",
                        "content": "대지면적이 200제곱미터 이상인 건축물"
                    },
                    {
                        "id": "subp-001-011-002",
                        "article_id": "art-001-011",
                        "type": "호",
                        "number": "2",
                        "content": "연면적이 500제곱미터 이상인 건축물"
                    }
                ],
                "related_articles": ["art-001-014", "art-001-015"]
            },
            {
                "id": "art-001-014",
                "law_id": "law-001",
                "number": "제14조",
                "title": "건축신고",
                "content": "제11조에도 불구하고 다음 각 호의 어느 하나에 해당하는 건축물을 건축하려는 자는 행정기관의 장에게 신고하여야 한다.",
                "subparagraphs": [
                    {
                        "id": "subp-001-014-001",
                        "article_id": "art-001-014",
                        "type": "호",
                        "number": "1",
                        "content": "대지면적이 200제곱미터 미만인 건축물"
                    }
                ],
                "related_articles": ["art-001-011"]
            }
        ]
    },
    {
        "id": "law-002",
        "name": "도시계획법",
        "type": "법률",
        "enactment_date": "1962-01-20",
        "amendment_date": "2023-12-31",
        "category": ["건설", "도시계획"],
        "articles": [
            {
                "id": "art-002-001",
                "law_id": "law-002",
                "number": "제1조",
                "title": "목적",
                "content": "이 법은 도시의 계획적이고 체계적인 개발·정비 및 관리를 도모하고, 쾌적한 도시환경을 조성하여 국민의 복리 증진에 이바지함을 목적으로 한다.",
                "subparagraphs": [],
                "related_articles": []
            },
            {
                "id": "art-002-056",
                "law_id": "law-002",
                "number": "제56조",
                "title": "개발행위의 허가",
                "content": "도시계획시설부지, 개발제한구역, 시가화조정구역 또는 그 밖에 대통령령으로 정하는 지역에서 건축물의 건축, 공작물의 설치, 토지의 형질변경, 토석의 채취, 물건을 쌓아 두는 행위(이하 \"개발행위\"라 한다)를 하려는 자는 특별시장·광역시장·특별자치시장·도지사 또는 시장·군수·구청장의 허가를 받아야 한다.",
                "subparagraphs": [],
                "related_articles": []
            }
        ]
    },
    {
        "id": "law-003",
        "name": "전기사업법",
        "type": "법률",
        "enactment_date": "1990-01-13",
        "amendment_date": "2024-01-23",
        "category": ["에너지", "전기"],
        "articles": [
            {
                "id": "art-003-001",
                "law_id": "law-003",
                "number": "제1조",
                "title": "목적",
                "content": "이 법은 전기사업의 적정한 경쟁을 도모하고 전기사업의 건전한 발전을 촉진하여 전력의 안정적인 공급과 전기사용자의 이익을 보호함을 목적으로 한다.",
                "subparagraphs": [],
                "related_articles": []
            },
            {
                "id": "art-003-007",
                "law_id": "law-003",
                "number": "제7조",
                "title": "전기사업의 허가",
                "content": "전기사업을 경영하려는 자는 산업통상자원부장관의 허가를 받아야 한다. 다만, 발전사업의 경우에는 신고로 할 수 있다.",
                "subparagraphs": [
                    {
                        "id": "subp-003-007-001",
                        "article_id": "art-003-007",
                        "type": "항",
                        "number": "1",
                        "content": "발전설비의 용량이 1만킬로와트 이상인 경우"
                    }
                ],
                "related_articles": ["art-003-008"]
            },
            {
                "id": "art-003-008",
                "law_id": "law-003",
                "number": "제8조",
                "title": "발전사업의 신고",
                "content": "발전사업을 경영하려는 자는 산업통상자원부장관에게 신고하여야 한다.",
                "subparagraphs": [],
                "related_articles": ["art-003-007"]
            }
        ]
    },
    {
        "id": "law-004",
        "name": "신에너지 및 재생에너지 개발·이용·보급 촉진법",
        "type": "법률",
        "enactment_date": "1987-12-04",
        "amendment_date": "2023-12-31",
        "category": ["에너지", "신재생에너지"],
        "articles": [
            {
                "id": "art-004-001",
                "law_id": "law-004",
                "number": "제1조",
                "title": "목적",
                "content": "이 법은 신에너지 및 재생에너지의 기술개발·이용 및 보급을 촉진하여 에너지원의 다양화와 에너지 안보 강화에 이바지함을 목적으로 한다.",
                "subparagraphs": [],
                "related_articles": []
            },
            {
                "id": "art-004-002",
                "law_id": "law-004",
                "number": "제2조",
                "title": "정의",
                "content": "이 법에서 사용하는 용어의 뜻은 다음과 같다.",
                "subparagraphs": [
                    {
                        "id": "subp-004-002-001",
                        "article_id": "art-004-002",
                        "type": "항",
                        "number": "1",
                        "content": "\"신에너지\"란 기존의 화석연료를 변환 이용하거나 수소·연료전지를 이용하는 에너지 및 석탄을 액화하거나 기체화하여 이용하는 에너지를 말한다."
                    },
                    {
                        "id": "subp-004-002-002",
                        "article_id": "art-004-002",
                        "type": "항",
                        "number": "2",
                        "content": "\"재생에너지\"란 햇빛, 물, 지열, 강수, 생물유기체 등 재생 가능한 에너지를 변환하여 이용하는 에너지를 말한다."
                    }
                ],
                "related_articles": []
            },
            {
                "id": "art-004-012",
                "law_id": "law-004",
                "number": "제12조",
                "title": "신재생에너지 발전사업",
                "content": "신재생에너지를 이용한 발전사업을 하려는 자는 전기사업법 제7조 및 제8조에 따라 허가를 받거나 신고를 하여야 한다.",
                "subparagraphs": [],
                "related_articles": ["law-003"]
            }
        ]
    },
    {
        "id": "law-005",
        "name": "환경영향평가법",
        "type": "법률",
        "enactment_date": "1999-12-31",
        "amendment_date": "2023-12-31",
        "category": ["환경", "평가"],
        "articles": [
            {
                "id": "art-005-001",
                "law_id": "law-005",
                "number": "제1조",
                "title": "목적",
                "content": "이 법은 환경영향평가를 통하여 개발사업으로 인한 환경상의 피해를 사전에 예방하고 환경을 적정하게 관리·보전함으로써 국민의 건강하고 쾌적한 생활환경을 확보하는 데 이바지함을 목적으로 한다.",
                "subparagraphs": [],
                "related_articles": []
            },
            {
                "id": "art-005-004",
                "law_id": "law-005",
                "number": "제4조",
                "title": "환경영향평가 대상사업",
                "content": "환경부장관은 다음 각 호의 어느 하나에 해당하는 사업을 환경영향평가 대상사업으로 지정한다.",
                "subparagraphs": [
                    {
                        "id": "subp-005-004-001",
                        "article_id": "art-005-004",
                        "type": "호",
                        "number": "1",
                        "content": "발전소 건설사업 중 발전용량이 1만킬로와트 이상인 사업"
                    },
                    {
                        "id": "subp-005-004-002",
                        "article_id": "art-005-004",
                        "type": "호",
                        "number": "2",
                        "content": "도로 건설사업 중 연장 1킬로미터 이상인 사업"
                    }
                ],
                "related_articles": []
            }
        ]
    },
    {
        "id": "law-006",
        "name": "산지관리법",
        "type": "법률",
        "enactment_date": "1994-01-07",
        "amendment_date": "2023-12-31",
        "category": ["환경", "산지"],
        "articles": [
            {
                "id": "art-006-001",
                "law_id": "law-006",
                "number": "제1조",
                "title": "목적",
                "content": "이 법은 산지의 보전·이용 및 관리에 관한 사항을 규정하여 산지의 공익기능을 증진하고 산지자원을 보전함으로써 국민경제의 건전한 발전에 이바지함을 목적으로 한다.",
                "subparagraphs": [],
                "related_articles": []
            },
            {
                "id": "art-006-014",
                "law_id": "law-006",
                "number": "제14조",
                "title": "산지전용허가",
                "content": "산지전용을 하려는 자는 산림청장의 허가를 받아야 한다. 다만, 다음 각 호의 어느 하나에 해당하는 경우에는 신고로 할 수 있다.",
                "subparagraphs": [
                    {
                        "id": "subp-006-014-001",
                        "article_id": "art-006-014",
                        "type": "호",
                        "number": "1",
                        "content": "산지전용면적이 1천제곱미터 미만인 경우"
                    }
                ],
                "related_articles": []
            }
        ]
    }
]


def get_all_laws() -> List[LawData]:
    """모든 법령 데이터 반환"""
    return MOCK_LAWS


def get_law_by_id(law_id: str) -> LawData | None:
    """법령 ID로 법령 데이터 조회"""
    for law in MOCK_LAWS:
        if law["id"] == law_id:
            return law
    return None


def search_laws_by_keyword(keyword: str) -> List[LawData]:
    """키워드로 법령 검색"""
    keyword_lower = keyword.lower()
    results = []
    
    for law in MOCK_LAWS:
        # 법령명 검색
        if keyword_lower in law["name"].lower():
            results.append(law)
            continue
        
        # 카테고리 검색
        if any(keyword_lower in cat.lower() for cat in law["category"]):
            results.append(law)
            continue
        
        # 조문 내용 검색
        for article in law.get("articles", []):
            if keyword_lower in article.get("content", "").lower():
                if law not in results:
                    results.append(law)
                break
    
    return results


def get_article_by_id(article_id: str) -> Dict[str, Any] | None:
    """조문 ID로 조문 데이터 조회"""
    for law in MOCK_LAWS:
        for article in law.get("articles", []):
            if article["id"] == article_id:
                return article
    return None

