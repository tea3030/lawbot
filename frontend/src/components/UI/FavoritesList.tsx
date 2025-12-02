import React, { useState } from "react";
import { useFavorites, type FavoriteMessage } from "../../hooks/useFavorites";
import { formatDateTime } from "../../utils/date";

interface FavoritesListProps {
  onSelect?: (message: FavoriteMessage) => void;
  onClose?: () => void;
}

export const FavoritesList: React.FC<FavoritesListProps> = ({
  onSelect,
  onClose,
}) => {
  const { favorites, removeFavorite } = useFavorites();
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const handleRemove = (e: React.MouseEvent, messageId: string) => {
    e.stopPropagation();
    if (confirm("즐겨찾기에서 제거하시겠습니까?")) {
      removeFavorite(messageId);
    }
  };

  const handleSelect = (message: FavoriteMessage) => {
    setSelectedId(message.id);
    onSelect?.(message);
  };

  if (favorites.length === 0) {
    return (
      <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
        <p className="text-slate-500">저장된 즐겨찾기가 없습니다.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 max-h-[70vh] overflow-y-auto">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-slate-900">즐겨찾기</h2>
        {onClose && (
          <button
            onClick={onClose}
            className="text-slate-500 hover:text-slate-700"
          >
            ✕
          </button>
        )}
      </div>
      <div className="space-y-3">
        {favorites.map((favorite) => (
          <div
            key={favorite.id}
            className={`p-4 rounded-lg border cursor-pointer transition-colors ${
              selectedId === favorite.id
                ? "border-indigo-500 bg-indigo-50"
                : "border-slate-200 hover:border-indigo-300 hover:bg-slate-50"
            }`}
            onClick={() => handleSelect(favorite)}
          >
            <div className="flex items-start justify-between gap-2">
              <div className="flex-1">
                <p className="text-sm text-slate-500 mb-2">
                  {formatDateTime(favorite.savedAt)}
                </p>
                <p className="text-slate-900 line-clamp-3">
                  {favorite.content}
                </p>
                {favorite.sources && favorite.sources.length > 0 && (
                  <div className="mt-2 text-xs text-indigo-600">
                    {favorite.sources.map((source) => (
                      <span key={source.lawId} className="block">
                        📄 {source.title} {source.article}
                      </span>
                    ))}
                  </div>
                )}
              </div>
              <button
                onClick={(e) => handleRemove(e, favorite.id)}
                className="p-2 text-red-500 hover:text-red-700 hover:bg-red-50 rounded"
                title="즐겨찾기 제거"
              >
                <svg
                  className="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

