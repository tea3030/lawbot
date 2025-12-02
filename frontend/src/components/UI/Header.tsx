import React, { useState } from "react";
import { FavoritesList } from "./FavoritesList";

export const Header: React.FC = () => {
  const [showFavorites, setShowFavorites] = useState(false);

  return (
    <>
      <header className="bg-white shadow-sm border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 bg-indigo-600 rounded-lg">
                <span className="text-white font-bold text-lg">법</span>
              </div>
              <div className="flex flex-col">
                <h1 className="text-xl font-bold text-slate-900">LawChat</h1>
                <p className="text-xs text-slate-500">법령 Q&A 챗봇</p>
              </div>
            </div>
            <nav className="flex items-center gap-6">
              <button
                onClick={() => setShowFavorites(!showFavorites)}
                className="text-slate-600 hover:text-indigo-600 transition-colors flex items-center gap-2"
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                  />
                </svg>
                즐겨찾기
              </button>
              <a
                href="#"
                className="text-slate-600 hover:text-indigo-600 transition-colors"
              >
                대화 목록
              </a>
              <a
                href="#"
                className="text-slate-600 hover:text-indigo-600 transition-colors"
              >
                법령 검색
              </a>
            </nav>
          </div>
        </div>
      </header>
      {showFavorites && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl max-w-2xl w-full max-h-[80vh] overflow-hidden">
            <FavoritesList onClose={() => setShowFavorites(false)} />
          </div>
        </div>
      )}
    </>
  );
};

