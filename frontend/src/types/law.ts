export interface LawArticle {
  id: string;
  lawId: string;
  number: string;
  title: string;
  content: string;
}

export interface Law {
  id: string;
  name: string;
  type: string;
  enactmentDate: string;
  amendmentDate?: string;
  category: string[];
  articles: LawArticle[];
}

