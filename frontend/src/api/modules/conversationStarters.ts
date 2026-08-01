import { api, isBackendConfigured } from "../client";

export interface ConversationStarterSuggestion {
  text: string;
  confidence: number;
}

export interface ConversationStarterResponse {
  suggestions: ConversationStarterSuggestion[];
  target_user_id: string;
  target_user_name: string;
}

export const fallbackConversationStarters = (): ConversationStarterSuggestion[] => [
  {
    text: "Hi! I'd love to connect and learn more about your work.",
    confidence: 0.7,
  },
  {
    text: "I noticed we're both working on interesting projects. Would you like to collaborate?",
    confidence: 0.6,
  },
  {
    text: "Your profile caught my eye. What are you currently building?",
    confidence: 0.65,
  },
];

export const conversationStartersApi = {
  generate: async (targetUserId: string): Promise<ConversationStarterResponse> => {
    if (!isBackendConfigured()) {
      return {
        suggestions: fallbackConversationStarters(),
        target_user_id: targetUserId,
        target_user_name: "your connection",
      };
    }
    return api.post<ConversationStarterResponse>("/api/conversation-starters", {
      target_user_id: targetUserId,
    });
  },
};
