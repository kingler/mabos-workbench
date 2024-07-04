import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const createKnowledgeBase = async () => {
  const response = await apiClient.post('/knowledge_bases/');
  return response.data;
};

export const addSymbolicKnowledge = async (kbId: string, item: any) => {
  const response = await apiClient.post(`/knowledge_bases/${kbId}/symbolic`, item);
  return response.data;
};

export const addNeuralKnowledge = async (kbId: string, item: any) => {
  const response = await apiClient.post(`/knowledge_bases/${kbId}/neural`, item);
  return response.data;
};

export const queryKnowledgeBase = async (kbId: string, query: string) => {
  const response = await apiClient.post(`/knowledge_bases/${kbId}/query`, { query });
  return response.data;
};

export const generatePlan = async (kbId: string, goal: string, initialState: any) => {
  const response = await apiClient.post(`/knowledge_bases/${kbId}/plan`, { goal, initial_state: initialState });
  return response.data;
};

export const reasonWithKnowledgeBase = async (kbId: string, context: any) => {
  const response = await apiClient.post(`/knowledge_bases/${kbId}/reason`, { context });
  return response.data;
};

export const simulateAction = async (kbId: string, action: string, state: any) => {
  const response = await apiClient.post(`/knowledge_bases/${kbId}/simulate`, { action, state });
  return response.data;
};

// Add more API functions as needed

export default apiClient;