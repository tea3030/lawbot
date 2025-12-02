import React from "react";

export const Footer: React.FC = () => {
  return (
    <footer className="bg-slate-50 border-t border-slate-200 mt-auto">
      <div className="max-w-7xl mx-auto px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between">
          <div className="text-sm text-slate-600">
            <p className="font-medium">LawChat</p>
            <p className="text-xs mt-1">
              법령 기반 질의응답 웹 애플리케이션
            </p>
          </div>
          <div className="text-xs text-slate-500 text-right">
            <p>
              이 답변은 참고용이며, 정확한 법적 판단은 전문가와 상담하세요.
            </p>
            <p className="mt-1">© 2025 LawChat. All rights reserved.</p>
          </div>
        </div>
      </div>
    </footer>
  );
};

