import React, { useState } from "react";

interface FeedbackFormProps {
  messageId?: string;
  onClose?: () => void;
}

export const FeedbackForm: React.FC<FeedbackFormProps> = ({
  messageId,
  onClose,
}) => {
  const [rating, setRating] = useState<number | null>(null);
  const [comment, setComment] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // 피드백 데이터 저장 (로컬 스토리지 또는 API)
    const feedback = {
      messageId,
      rating,
      comment,
      timestamp: new Date().toISOString(),
    };

    // 로컬 스토리지에 저장 (실제로는 API로 전송)
    const existingFeedback = JSON.parse(
      localStorage.getItem("lawchat_feedback") || "[]"
    );
    existingFeedback.push(feedback);
    localStorage.setItem("lawchat_feedback", JSON.stringify(existingFeedback));

    setSubmitted(true);
    setTimeout(() => {
      onClose?.();
    }, 2000);
  };

  if (submitted) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
        <p className="text-green-700 font-medium">피드백이 전송되었습니다. 감사합니다!</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-2">
          이 답변이 도움이 되었나요?
        </label>
        <div className="flex gap-2">
          {[1, 2, 3, 4, 5].map((num) => (
            <button
              key={num}
              type="button"
              onClick={() => setRating(num)}
              className={`w-10 h-10 rounded-lg transition-colors ${
                rating === num
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-100 text-slate-600 hover:bg-slate-200"
              }`}
            >
              {num === 5 ? "👍" : num === 1 ? "👎" : "😐"}
            </button>
          ))}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-slate-700 mb-2">
          추가 의견 (선택사항)
        </label>
        <textarea
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          rows={3}
          placeholder="개선 사항이나 의견을 남겨주세요..."
          maxLength={500}
        />
      </div>

      <div className="flex gap-2">
        <button
          type="submit"
          disabled={rating === null}
          className="flex-1 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          제출
        </button>
        {onClose && (
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors"
          >
            취소
          </button>
        )}
      </div>
    </form>
  );
};

