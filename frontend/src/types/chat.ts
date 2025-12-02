export interface LawReference {
  lawId: string;
  article?: string;
  title?: string;
  url?: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  createdAt: string;
  sources?: LawReference[];
}

