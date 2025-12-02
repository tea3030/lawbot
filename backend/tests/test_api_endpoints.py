"""API 엔드포인트 테스트"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """루트 엔드포인트 테스트"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "status" in data


def test_health_check():
    """헬스 체크 엔드포인트 테스트"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_search_laws_empty_keyword():
    """빈 키워드로 법령 검색 테스트"""
    response = client.get("/api/laws/search?keyword=")
    assert response.status_code == 400


def test_search_laws_valid_keyword():
    """유효한 키워드로 법령 검색 테스트"""
    response = client.get("/api/laws/search?keyword=건축")
    assert response.status_code == 200
    data = response.json()
    assert "laws" in data
    assert "count" in data
    assert isinstance(data["laws"], list)


def test_get_law_by_id():
    """법령 ID로 조회 테스트"""
    response = client.get("/api/laws/law-001")
    assert response.status_code == 200
    data = response.json()
    assert "law" in data
    assert data["law"]["id"] == "law-001"


def test_get_law_not_found():
    """존재하지 않는 법령 조회 테스트"""
    response = client.get("/api/laws/law-999")
    assert response.status_code == 404


def test_chat_message_empty():
    """빈 메시지로 채팅 테스트"""
    response = client.post("/api/chat/", json={"message": ""})
    assert response.status_code == 400


def test_chat_message_too_long():
    """너무 긴 메시지로 채팅 테스트"""
    long_message = "a" * 1001
    response = client.post("/api/chat/", json={"message": long_message})
    assert response.status_code == 400


def test_chat_message_valid():
    """유효한 메시지로 채팅 테스트"""
    # OpenAI API 키가 없으면 503 에러가 발생할 수 있음
    response = client.post(
        "/api/chat/",
        json={"message": "건축법에 대해 알려주세요"}
    )
    # 200 또는 503 (OpenAI API 키 없음)
    assert response.status_code in [200, 503]


def test_create_conversation():
    """대화 세션 생성 테스트"""
    response = client.post("/api/conversations", json={"title": "테스트 대화"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "title" in data


def test_get_conversations():
    """대화 세션 목록 조회 테스트"""
    response = client.get("/api/conversations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_conversation_not_found():
    """존재하지 않는 대화 세션 조회 테스트"""
    response = client.get("/api/conversations/non-existent-id")
    assert response.status_code == 404

