import { useState, useEffect } from "react";
import type { ChatMessage } from "../types/chat";

const FAVORITES_KEY = "lawchat_favorites";

export interface FavoriteMessage extends ChatMessage {
  savedAt: string;
  note?: string;
}

export const useFavorites = () => {
  const [favorites, setFavorites] = useState<FavoriteMessage[]>([]);

  // 로컬 스토리지에서 즐겨찾기 불러오기
  useEffect(() => {
    try {
      const stored = localStorage.getItem(FAVORITES_KEY);
      if (stored) {
        setFavorites(JSON.parse(stored));
      }
    } catch (error) {
      console.error("즐겨찾기 불러오기 실패:", error);
    }
  }, []);

  // 즐겨찾기 추가
  const addFavorite = (message: ChatMessage, note?: string) => {
    const favorite: FavoriteMessage = {
      ...message,
      savedAt: new Date().toISOString(),
      note,
    };

    const updated = [favorite, ...favorites];
    setFavorites(updated);
    
    try {
      localStorage.setItem(FAVORITES_KEY, JSON.stringify(updated));
    } catch (error) {
      console.error("즐겨찾기 저장 실패:", error);
    }
  };

  // 즐겨찾기 제거
  const removeFavorite = (messageId: string) => {
    const updated = favorites.filter((fav) => fav.id !== messageId);
    setFavorites(updated);
    
    try {
      localStorage.setItem(FAVORITES_KEY, JSON.stringify(updated));
    } catch (error) {
      console.error("즐겨찾기 삭제 실패:", error);
    }
  };

  // 즐겨찾기 확인
  const isFavorite = (messageId: string) => {
    return favorites.some((fav) => fav.id === messageId);
  };

  return {
    favorites,
    addFavorite,
    removeFavorite,
    isFavorite,
  };
};

