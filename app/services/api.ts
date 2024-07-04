import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Update with your FastAPI server URL
});

export const fetchViewModel = async (viewName: string) => {
  const response = await api.get(`/${viewName}`);
  return response.data;
};

// Agents Endpoints
export const createAgent = async (agentData: any) => {
  const response = await api.post('/v1/agents/agents/', agentData);
  return response.data;
};

export const listAgents = async () => {
  const response = await api.get('/v1/agents/agents/');
  return response.data;
};

export const getAgent = async (agentId: string) => {
  const response = await api.get(`/v1/agents/agents/${agentId}`);
  return response.data;
};

export const updateAgent = async (agentId: string, agentData: any) => {
  const response = await api.put(`/v1/agents/${agentId}`, agentData);
  return response.data;
};

export const deleteAgent = async (agentId: string) => {
  const response = await api.delete(`/v1/agents/${agentId}`);
  return response.data;
};

export const addBelief = async (agentId: string, beliefData: any) => {
  const response = await api.post(`/v1/agents/agents/${agentId}/beliefs`, beliefData);
  return response.data;
};

export const addDesire = async (agentId: string, desireData: any) => {
  const response = await api.post(`/v1/agents/agents/${agentId}/desires`, desireData);
  return response.data;
};

export const addIntention = async (agentId: string, intentionData: any) => {
  const response = await api.post(`/v1/agents/agents/${agentId}/intentions`, intentionData);
  return response.data;
};

// Environmental Agent Endpoints
export const createEnvironmentalAgent = async (agentData: any) => {
  const response = await api.post('/v1/agents/environmental', agentData);
  return response.data;
};

export const updateEnvironmentState = async (agentId: string, stateData: any) => {
  const response = await api.put(`/v1/agents/environmental/${agentId}/update_state`, stateData);
  return response.data;
};

// Proactive and Reactive Agent Endpoints
export const createProactiveAgent = async (agentData: any) => {
  const response = await api.post('/v1/agents/proactive', agentData);
  return response.data;
};

export const proposeProactiveStrategy = async (agentId: string, strategyData: any) => {
  const response = await api.post(`/v1/agents/proactive/${agentId}/propose_strategy`, strategyData);
  return response.data;
};

export const createReactiveAgent = async (agentData: any) => {
  const response = await api.post('/v1/agents/reactive', agentData);
  return response.data;
};

export const handleReactiveEvent = async (agentId: string, eventData: any) => {
  const response = await api.post(`/v1/agents/reactive/${agentId}/handle_event`, eventData);
  return response.data;
};

// Goals Endpoints
export const createGoal = async (goalData: any) => {
  const response = await api.post('/v1/goals/goals/', goalData);
  return response.data;
};

export const listGoals = async () => {
  const response = await api.get('/v1/goals/goals/');
  return response.data;
};

export const getGoal = async (goalId: string) => {
  const response = await api.get(`/v1/goals/goals/${goalId}`);
  return response.data;
};

export const decomposeGoal = async (goalId: string, decomposeData: any) => {
  const response = await api.post(`/v1/goals/goals/${goalId}/decompose`, decomposeData);
  return response.data;
};

export const updateGoalStatus = async (goalId: string, statusData: any) => {
  const response = await api.put(`/v1/goals/goals/${goalId}/status`, statusData);
  return response.data;
};

// Plans Endpoints
export const createPlan = async (planData: any) => {
  const response = await api.post('/v1/plans/plans/', planData);
  return response.data;
};

export const listPlans = async () => {
  const response = await api.get('/v1/plans/plans/');
  return response.data;
};

export const getPlan = async (planId: string) => {
  const response = await api.get(`/v1/plans/plans/${planId}`);
  return response.data;
};

export const addPlanStep = async (planId: string, stepData: any) => {
  const response = await api.post(`/v1/plans/plans/${planId}/steps`, stepData);
  return response.data;
};

export const updateStepStatus = async (planId: string, stepId: string, statusData: any) => {
  const response = await api.put(`/v1/plans/plans/${planId}/steps/${stepId}`, statusData);
  return response.data;
};

export const executePlan = async (planId: string) => {
  const response = await api.post(`/v1/plans/plans/${planId}/execute`);
  return response.data;
};

// Knowledge Bases Endpoints
export const listKnowledgeBases = async () => {
  const response = await api.get('/v1/knowledge_bases/knowledge_bases/');
  return response.data;
};

export const createKnowledgeBase = async (kbData: any) => {
  const response = await api.post('/v1/knowledge_bases/knowledge_bases/', kbData);
  return response.data;
};

export const getKnowledgeBase = async (kbId: string) => {
  const response = await api.get(`/v1/knowledge_bases/knowledge_bases/${kbId}`);
  return response.data;
};

export const addSymbolicKnowledge = async (kbId: string, knowledgeData: any) => {
  const response = await api.post(`/v1/knowledge_bases/knowledge_bases/${kbId}/symbolic`, knowledgeData);
  return response.data;
};

export const addNeuralKnowledge = async (kbId: string, knowledgeData: any) => {
  const response = await api.post(`/v1/knowledge_bases/knowledge_bases/${kbId}/neural`, knowledgeData);
  return response.data;
};

export const queryKnowledgeBase = async (kbId: string, queryData: any) => {
  const response = await api.post(`/v1/knowledge_bases/knowledge_bases/${kbId}/query`, queryData);
  return response.data;
};

export const reason = async (kbId: string, reasonData: any) => {
  const response = await api.post(`/v1/knowledge_bases/knowledge_bases/${kbId}/reason`, reasonData);
  return response.data;
};

export const simulateAction = async (kbId: string, actionData: any) => {
  const response = await api.post(`/v1/knowledge_bases/knowledge_bases/${kbId}/simulate`, actionData);
  return response.data;
};

export const generatePlan = async (kbId: string, planData: any) => {
  const response = await api.post(`/v1/knowledge_bases/knowledge_bases/${kbId}/plan`, planData);
  return response.data;
};

// Actions Endpoints
export const createAction = async (actionData: any) => {
  const response = await api.post('/v1/actions/', actionData);
  return response.data;
};

export const getAction = async (actionId: string) => {
  const response = await api.get(`/v1/actions/${actionId}`);
  return response.data;
};

export const updateAction = async (actionId: string, actionData: any) => {
  const response = await api.put(`/v1/actions/${actionId}`, actionData);
  return response.data;
};

export const deleteAction = async (actionId: string) => {
  const response = await api.delete(`/v1/actions/${actionId}`);
  return response.data;
};

export const executeAction = async (actionId: string) => {
  const response = await api.post(`/v1/actions/${actionId}/execute`);
  return response.data;
};

export const getAvailableActions = async (agentId: string) => {
  const response = await api.get(`/v1/agents/${agentId}/available_actions`);
  return response.data;
};

// Tasks Endpoints
export const createTask = async (taskData: any) => {
  const response = await api.post('/v1/tasks/', taskData);
  return response.data;
};

export const getTask = async (taskId: string) => {
  const response = await api.get(`/v1/tasks/${taskId}`);
  return response.data;
};

export const updateTask = async (taskId: string, taskData: any) => {
  const response = await api.put(`/v1/tasks/${taskId}`, taskData);
  return response.data;
};

export const deleteTask = async (taskId: string) => {
  const response = await api.delete(`/v1/tasks/${taskId}`);
  return response.data;
};

export const assignTask = async (taskId: string, agentId: string) => {
  const response = await api.post(`/v1/tasks/${taskId}/assign/${agentId}`);
  return response.data;
};

export const execute