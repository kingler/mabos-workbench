import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export interface StakeholderGoal {
  goal: string;
  priority: number;
  type: 'hard' | 'soft';
}

export interface OnboardingPayload {
  business_id: string;
  business_name: string;
  business_type: string;
  legal_name?: string;
  description?: string;
  jurisdiction?: string;
  stage?: string;
  value_propositions?: string[];
  customer_segments?: string[];
  revenue_streams?: string[];
  stakeholder_goals?: StakeholderGoal[];
  constraints?: string[];
  agent_roles: string[];
  sbvr_export: Record<string, unknown>;
}

export interface OnboardingResult {
  success: boolean;
  business_id: string;
  agent_ids?: string[];
  ontology_stats?: {
    concept_types: number;
    fact_types: number;
    rules: number;
    proof_tables: number;
  };
  error?: string;
  timestamp: string;
}

export interface OnboardingProgress {
  business_id: string;
  started_at: string;
  phases: Record<string, {
    status: 'pending' | 'in_progress' | 'completed' | 'failed' | 'skipped';
    started_at: string | null;
    completed_at: string | null;
    details?: string;
  }>;
  current_phase: string;
  overall_status: string;
}

const DEFAULT_AGENT_ROLES = [
  'ceo', 'cfo', 'coo', 'cmo', 'cto', 'hr', 'legal', 'strategy', 'knowledge',
];

/**
 * Submit business onboarding to the backend.
 * Creates business record, loads SBVR ontology, and creates agent nodes.
 */
export async function onboardBusiness(payload: OnboardingPayload): Promise<OnboardingResult> {
  const response = await api.post<OnboardingResult>('/api/businesses/onboard', {
    ...payload,
    agent_roles: payload.agent_roles || DEFAULT_AGENT_ROLES,
  });
  return response.data;
}

/**
 * Get onboarding progress for a business.
 */
export async function getOnboardingProgress(businessId: string): Promise<OnboardingProgress> {
  const response = await api.get<OnboardingProgress>(`/api/businesses/${businessId}/progress`);
  return response.data;
}

/**
 * Helper to convert form data into the onboarding payload format.
 * Comma-separated text fields are split into arrays.
 */
export function buildOnboardingPayload(formData: {
  name: string;
  legal_name: string;
  type: string;
  description: string;
  jurisdiction: string;
  stage: string;
  value_propositions: string;
  customer_segments: string;
  revenue_streams: string;
  stakeholder_goals?: StakeholderGoal[];
  constraints?: string;
}): Omit<OnboardingPayload, 'sbvr_export'> {
  const slugify = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
  const splitCsv = (s: string) => s.split(',').map(v => v.trim()).filter(Boolean);

  return {
    business_id: slugify(formData.name),
    business_name: formData.name,
    business_type: formData.type,
    legal_name: formData.legal_name,
    description: formData.description,
    jurisdiction: formData.jurisdiction,
    stage: formData.stage,
    value_propositions: splitCsv(formData.value_propositions),
    customer_segments: splitCsv(formData.customer_segments),
    revenue_streams: splitCsv(formData.revenue_streams),
    stakeholder_goals: formData.stakeholder_goals || [],
    constraints: formData.constraints
      ? formData.constraints.split('\n').map(c => c.trim()).filter(Boolean)
      : [],
    agent_roles: DEFAULT_AGENT_ROLES,
  };
}
