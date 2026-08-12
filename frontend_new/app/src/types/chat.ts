export interface Citation {
  page: number;
  text?: string;
}

export interface Message {
  id: number;
  role: "user" | "assistant";
  content: string;
  citations?: Citation[];
  created_at?: string;
}
