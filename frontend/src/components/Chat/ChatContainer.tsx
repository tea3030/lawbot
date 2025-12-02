import { FormEvent, useState } from "react";

import { useChat } from "../../hooks/useChat";
import { useFavorites } from "../../hooks/useFavorites";
import { FeedbackForm } from "../UI/FeedbackForm";
import type { ChatMessage } from "../../types/chat";

export const ChatContainer = () => {
  const { messages, isLoading, ask } = useChat();
  const { addFavorite, removeFavorite, isFavorite } = useFavorites();
  const [text, setText] = useState("");
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [feedbackMessageId, setFeedbackMessageId] = useState<string | null>(null);

  const handleCopy = async (message: ChatMessage) => {
    try {
      await navigator.clipboard.writeText(message.content);
      setCopiedId(message.id);
      setTimeout(() => setCopiedId(null), 2000);
    } catch (error) {
      console.error("복사 실패:", error);
    }
  };

  const handleToggleFavorite = (message: ChatMessage) => {
    if (isFavorite(message.id)) {
      removeFavorite(message.id);
    } else {
      addFavorite(message);
    }
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await ask(text);
    setText("");
  };

  return (
    <div className="flex flex-col gap-4 w-full max-w-3xl mx-auto">
      <div className="bg-white rounded-2xl shadow-lg p-6 h-[60vh] min-h-[500px] overflow-y-auto space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="w-20 h-20 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
              <span className="text-3xl">⚖️</span>
            </div>
            <p className="text-slate-600 text-xl font-medium mb-2">
              안녕하세요!
            </p>
            <p className="text-slate-500">
              인허가 절차나 관련 법령을 질문해보세요.
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`rounded-2xl px-4 py-3 text-base leading-relaxed relative group ${
                message.role === "assistant"
                  ? "bg-indigo-50 text-indigo-900"
                  : "bg-slate-100 text-slate-900 text-right"
              }`}
            >
              <div className="whitespace-pre-wrap break-words">
                {message.content}
              </div>
              {message.sources && message.sources.length > 0 && (
                <div className="mt-2 pt-2 border-t border-indigo-200 text-xs text-indigo-600">
                  {message.sources.map((source) => (
                    <span key={source.lawId} className="block">
                      📄 {source.title ?? source.lawId}{" "}
                      {source.article ?? ""}
                    </span>
                  ))}
                </div>
              )}
              <div className="absolute top-2 right-2 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                {message.role === "assistant" && (
                  <button
                    onClick={() => setFeedbackMessageId(message.id)}
                    className={`p-2 rounded-lg transition-colors ${
                      message.role === "assistant"
                        ? "bg-indigo-100 hover:bg-indigo-200"
                        : "bg-slate-200 hover:bg-slate-300"
                    }`}
                    title="피드백 남기기"
                  >
                    <svg
                      className="w-4 h-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"
                      />
                    </svg>
                  </button>
                )}
                <button
                  onClick={() => handleToggleFavorite(message)}
                  className={`p-2 rounded-lg transition-colors ${
                    message.role === "assistant"
                      ? "bg-indigo-100 hover:bg-indigo-200"
                      : "bg-slate-200 hover:bg-slate-300"
                  } ${isFavorite(message.id) ? "text-red-500" : "text-slate-600"}`}
                  title={isFavorite(message.id) ? "즐겨찾기 제거" : "즐겨찾기 추가"}
                >
                  <svg
                    className="w-4 h-4"
                    fill={isFavorite(message.id) ? "currentColor" : "none"}
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
                </button>
                <button
                  onClick={() => handleCopy(message)}
                  className={`p-2 rounded-lg transition-colors ${
                    message.role === "assistant"
                      ? "bg-indigo-100 hover:bg-indigo-200"
                      : "bg-slate-200 hover:bg-slate-300"
                  }`}
                  title="복사하기"
                >
                  {copiedId === message.id ? (
                    <svg
                      className="w-4 h-4 text-green-600"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M5 13l4 4L19 7"
                      />
                    </svg>
                  ) : (
                    <svg
                      className="w-4 h-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                      />
                    </svg>
                  )}
                </button>
              </div>
            </div>
          ))
        )}
      </div>
      {feedbackMessageId && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl max-w-md w-full p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-slate-900">피드백 남기기</h3>
              <button
                onClick={() => setFeedbackMessageId(null)}
                className="text-slate-500 hover:text-slate-700"
              >
                ✕
              </button>
            </div>
            <FeedbackForm
              messageId={feedbackMessageId}
              onClose={() => setFeedbackMessageId(null)}
            />
          </div>
        </div>
      )}
      <form
        onSubmit={handleSubmit}
        className="flex gap-3 bg-white p-3 rounded-2xl shadow-lg"
      >
        <input
          className="flex-1 border-0 focus:outline-none px-4 text-base"
          type="text"
          value={text}
          onChange={(event) => setText(event.target.value)}
          placeholder="질문을 입력하세요"
        />
        <button
          type="submit"
          className="bg-indigo-600 text-white px-6 py-3 rounded-full disabled:opacity-60 text-base font-medium transition-colors hover:bg-indigo-700 active:bg-indigo-800"
          disabled={isLoading}
        >
          {isLoading ? (
            <span className="flex items-center gap-2">
              <svg
                className="animate-spin h-4 w-4"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              전송 중...
            </span>
          ) : (
            "전송"
          )}
        </button>
      </form>
    </div>
  );
};

