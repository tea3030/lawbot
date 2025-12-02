"""OpenAI API 연동 서비스"""
from typing import List, Optional, Dict, Any
from openai import OpenAI
from app.core.security import get_openai_api_key
from app.services.law_service import LawService


class OpenAIService:
    """OpenAI API 서비스"""
    
    def __init__(self):
        self.client = OpenAI(api_key=get_openai_api_key())
        # 최신 OpenAI 모델 (사용 가능 여부는 계정/시점에 따라 다를 수 있음)
        self.model = "gpt-5.1-2025-11-13"
    
    # ---------- 법령 세트(법률 + 시행령 + 시행규칙 + 조례) 구성 로직 ----------
    @staticmethod
    def _normalize_law_name(name: str) -> str:
        """법령명을 기반으로 '기본법 이름'만 추출 (시행령/시행규칙/조례 접미어 제거)"""
        if not name:
            return ""
        suffixes = ["시행령", "시행규칙", "시행세칙", "조례", "규칙"]
        base = name.strip()
        for s in suffixes:
            if base.endswith(s):
                return base[: -len(s)].strip()
        return base

    def _build_law_sets(self, laws: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """법률 + 시행령 + 시행규칙 + 조례를 한 세트로 묶기

        반환 형식(프롬프트용):
        [
          {
            "base_name": "건축법",
            "main": {...},         # 가능한 경우: 기본 법률
            "children": [ {...}, {...} ]  # 시행령/시행규칙/조례 등
          },
          ...
        ]
        """
        groups: Dict[str, Dict[str, Any]] = {}

        for law in laws:
            name = law.get("name", "") or ""
            base_name = self._normalize_law_name(name)
            if not base_name:
                continue

            group = groups.setdefault(
                base_name,
                {"base_name": base_name, "main": None, "children": []},
            )

            law_type = (law.get("type") or "").strip()

            # '법' 또는 '법률'이 기본법에 해당할 가능성이 크다고 보고 main으로 우선 배치
            if "법" in law_type and "시행" not in law_type and group["main"] is None:
                group["main"] = law
            else:
                group["children"].append(law)

        # main 이 없는 세트는 children 중 하나를 main 으로 승격
        for g in groups.values():
            if g["main"] is None and g["children"]:
                g["main"] = g["children"][0]
                g["children"] = g["children"][1:]

        # 리스트로 변환
        return list(groups.values())
    
    def create_law_prompt(self, question: str, laws: List[dict]) -> str:
        """
        법령 컨텍스트를 포함한 프롬프트 생성
        
        Args:
            question: 사용자 질문
            laws: 관련 법령 데이터 리스트
        
        Returns:
            프롬프트 문자열
        """
        # 법률 + 시행령 + 시행규칙 + 조례를 세트로 구성
        law_sets = self._build_law_sets(laws)

        law_context = ""
        
        for law_set in law_sets[:5]:  # 최대 5개 세트만 사용
            main = law_set.get("main")
            children = law_set.get("children", [])
            if not main:
                continue

            law_context += f"\n\n## {law_set['base_name']} (기본법: {main.get('name', '')} / {main.get('type', '')})\n"
            law_context += f"최신 개정일: {main.get('amendment_date', 'N/A')}\n"

            # 기본법 조문
            for article in main.get("articles", [])[:3]:  # 각 법령의 최대 3개 조문
                law_context += f"\n### {article.get('number', '')} {article.get('title', '')}\n"
                law_context += f"{article.get('content', '')}\n"
                
                # 항/호/목이 있으면 추가
                for subp in article.get("subparagraphs", [])[:2]:
                    law_context += f"\n{subp.get('type', '')} {subp.get('number', '')}. {subp.get('content', '')}\n"

            # 관련 시행령/시행규칙/조례 요약
            if children:
                law_context += "\n[관련 하위 법령]\n"
                for child in children[:3]:  # 최대 3개만 노출
                    law_context += f"- {child.get('name', '')} ({child.get('type', '')})\n"
        
        prompt = f"""당신은 법령 전문가 AI 비서입니다. 다음 법령 정보를 바탕으로 사용자의 질문에 정확하게 답변해주세요.

[법령 컨텍스트]
{law_context}

[사용자 질문]
{question}

답변 시 다음 사항을 지켜주세요:
1. 관련 법령과 조문을 명확히 인용해주세요. (예: 건축법 제11조)
2. 법률 용어는 가능한 쉽게 설명해주세요.
3. 인허가 절차가 있다면 단계별로 구분하여 설명해주세요.
4. 담당 기관이나 부서 정보도 포함해주세요.
5. 답변 마지막에는 반드시 "이 답변은 참고용이며, 정확한 법적 판단은 전문가와 상담하세요."라는 면책 문구를 포함해주세요.

답변:"""
        
        return prompt
    
    def ask_question(
        self,
        question: str,
        conversation_history: Optional[List[dict]] = None
    ) -> str:
        """
        사용자 질문에 대한 답변 생성
        
        Args:
            question: 사용자 질문
            conversation_history: 대화 히스토리 (선택)
        
        Returns:
            GPT 응답 텍스트
        """
        # 관련 법령 검색 (실제 API + 목업 fallback)
        related_laws = LawService.search_laws(question)
        
        # 프롬프트 생성
        prompt = self.create_law_prompt(question, related_laws)
        
        # 대화 히스토리 구성
        messages = []
        
        # 시스템 메시지
        messages.append({
            "role": "system",
            "content": "당신은 법령 전문가 AI 비서입니다. 제공된 법령 정보를 바탕으로 정확하고 명확한 답변을 제공합니다."
        })
        
        # 대화 히스토리 추가 (최근 5개만)
        if conversation_history:
            for msg in conversation_history[-5:]:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
        
        # 현재 질문
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        try:
            # OpenAI API 호출
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise Exception(f"OpenAI API 호출 실패: {str(e)}")
    
    def extract_law_references(self, response_text: str, laws: List[dict]) -> List[dict]:
        """
        응답 텍스트에서 법령 출처 추출
        
        Args:
            response_text: GPT 응답 텍스트
            laws: 관련 법령 리스트
        
        Returns:
            법령 출처 리스트
        """
        references = []
        
        # 법령명으로 출처 찾기
        for law in laws:
            if law["name"] in response_text:
                # 조문 번호 찾기 (예: "제11조", "제1조" 등)
                for article in law.get("articles", []):
                    article_number = article.get("number", "")
                    if article_number in response_text:
                        references.append({
                            "law_id": law["id"],
                            "title": law["name"],
                            "article": article_number
                        })
                        break
                
                # 조문을 찾지 못했으면 법령만 추가
                if not any(ref["law_id"] == law["id"] for ref in references):
                    references.append({
                        "law_id": law["id"],
                        "title": law["name"],
                        "article": None
                    })
        
        return references[:5]  # 최대 5개만 반환


# 싱글톤 인스턴스
_openai_service: Optional[OpenAIService] = None


def get_openai_service() -> OpenAIService:
    """OpenAI 서비스 인스턴스 가져오기"""
    global _openai_service
    if _openai_service is None:
        _openai_service = OpenAIService()
    return _openai_service

