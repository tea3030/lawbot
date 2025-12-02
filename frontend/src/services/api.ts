import axios from "axios";
import type { ChatMessage, LawReference } from "../types/chat";

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL ?? "http://localhost:8000",
  timeout: 30000, // ChatGPT API 응답 대기 시간 고려
  headers: {
    "Content-Type": "application/json",
  },
});

// 응답 인터셉터: 에러 처리
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // 서버에서 응답이 온 경우
      const { data, status } = error.response;
      const errorMessage = data?.message || data?.detail || "서버 오류가 발생했습니다.";
      
      // 에러 로깅
      console.error(`API Error [${status}]:`, errorMessage);
      
      // 에러 객체 확장
      error.message = errorMessage;
      error.errorData = data;
    } else if (error.request) {
      // 요청은 보냈지만 응답을 받지 못한 경우
      error.message = "서버에 연결할 수 없습니다. 네트워크를 확인해주세요.";
      console.error("Network Error:", error.message);
    } else {
      // 요청 설정 중 오류
      error.message = "요청을 처리하는 중 오류가 발생했습니다.";
      console.error("Request Error:", error.message);
    }
    
    return Promise.reject(error);
  }
);

// API 응답 타입
interface ChatResponse {
  id: string;
  content: string;
  law_references?: Array<{
    law_id: string;
    title?: string;
    article?: string;
  }>;
}

// 법령 검색 API
export const searchLaws = async (keyword: string) => {
  const { data } = await apiClient.get("/api/laws/search", {
    params: { keyword },
  });
  return data;
};

// 모든 법령 조회
export const getAllLaws = async () => {
  const { data } = await apiClient.get("/api/laws");
  return data;
};

// 법령 상세 조회
export const getLawById = async (lawId: string) => {
  const { data } = await apiClient.get(`/api/laws/${lawId}`);
  return data;
};

// 대화 세션 관련 API
export const createConversation = async (title?: string) => {
  const { data } = await apiClient.post("/api/conversations", { title });
  return data;
};

export const getConversations = async () => {
  const { data } = await apiClient.get("/api/conversations");
  return data;
};

export const getConversationMessages = async (conversationId: string) => {
  const { data } = await apiClient.get(`/api/conversations/${conversationId}/messages`);
  return data;
};

export const deleteConversation = async (conversationId: string) => {
  const { data } = await apiClient.delete(`/api/conversations/${conversationId}`);
  return data;
};

// 채팅 메시지 전송
export const sendChatMessage = async (payload: {
  message: string;
  conversation_id?: string;
}): Promise<ChatMessage> => {
  const { data } = await apiClient.post<ChatResponse>("/api/chat/", payload);
  
  // 백엔드 응답을 프론트엔드 타입으로 변환
  const lawReferences: LawReference[] | undefined = data.law_references?.map(
    (ref) => ({
      lawId: ref.law_id,
      title: ref.title,
      article: ref.article,
    })
  );

  return {
    id: data.id,
    role: "assistant",
    content: data.content,
    createdAt: new Date().toISOString(),
    sources: lawReferences,
  };
};

