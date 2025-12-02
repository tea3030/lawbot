import { useState, useCallback, useRef } from "react";

import { sendChatMessage } from "../services/api";
import type { ChatMessage } from "../types/chat";

export const useChat = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);

  const ask = useCallback(async (question: string) => {
    if (!question.trim()) {
      return;
    }

    // 이전 요청 취소
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
      createdAt: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    // 새로운 AbortController 생성
    abortControllerRef.current = new AbortController();

    try {
      const response = await sendChatMessage({ message: question });
      
      // 요청이 취소되었는지 확인
      if (abortControllerRef.current?.signal.aborted) {
        return;
      }

      const botMessage: ChatMessage = {
        id: response.id,
        role: "assistant",
        content: response.content,
        sources: response.sources,
        createdAt: response.createdAt,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error: any) {
      // 취소된 요청은 에러로 처리하지 않음
      if (error?.name === "AbortError" || abortControllerRef.current?.signal.aborted) {
        return;
      }

      let errorContent = "답변을 가져오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.";
      
      // 에러 메시지가 있으면 사용
      if (error?.message) {
        errorContent = error.message;
      } else if (error?.response?.data?.message) {
        errorContent = error.response.data.message;
      }
      
      const errorMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: errorContent,
        createdAt: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
      console.error("Chat error:", error);
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
  }, []);

  return {
    messages,
    isLoading,
    ask,
    clearMessages,
  };
};

