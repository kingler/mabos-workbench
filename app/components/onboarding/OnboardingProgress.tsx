import React, { useEffect, useState, useCallback } from 'react';
import { Box, Card, Flex, Text, Button, Badge } from '@radix-ui/themes';
import { CheckCircledIcon, CrossCircledIcon, ReloadIcon } from '@radix-ui/react-icons';

interface PhaseStatus {
  status: 'pending' | 'in_progress' | 'completed' | 'failed' | 'skipped';
  started_at: string | null;
  completed_at: string | null;
  details?: string;
}

interface ProgressData {
  business_id: string;
  started_at: string;
  phases: Record<string, PhaseStatus>;
  current_phase: string;
  overall_status: string;
}

interface OnboardingProgressProps {
  businessId: string;
  onFinish: () => void;
  onBack: () => void;
}

const PHASE_LABELS: Record<string, string> = {
  discovery: 'Discovery',
  architecture: 'Architecture',
  agents: 'Agent Activation',
  knowledge_graph: 'Knowledge Graph',
  launch: 'Launch',
};

const PHASE_DESCRIPTIONS: Record<string, string> = {
  discovery: 'Collecting business information',
  architecture: 'Generating TOGAF, BMC, and Tropos models',
  agents: 'Spawning C-suite and domain agents',
  knowledge_graph: 'Loading SBVR ontology into Neo4j',
  launch: 'Activating CEO agent and dashboard',
};

const PHASE_ORDER = ['discovery', 'architecture', 'agents', 'knowledge_graph', 'launch'];

const StatusBadge: React.FC<{ status: string }> = ({ status }) => {
  const colorMap: Record<string, 'green' | 'blue' | 'red' | 'gray' | 'orange'> = {
    completed: 'green',
    in_progress: 'blue',
    failed: 'red',
    pending: 'gray',
    skipped: 'orange',
  };
  return <Badge color={colorMap[status] || 'gray'}>{status.replace('_', ' ')}</Badge>;
};

const OnboardingProgress: React.FC<OnboardingProgressProps> = ({ businessId, onFinish, onBack }) => {
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProgress = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:8000/api/businesses/${businessId}/progress`);
      if (response.ok) {
        const data = await response.json();
        setProgress(data);
      } else {
        // If endpoint doesn't exist yet, show a pending state
        setProgress({
          business_id: businessId,
          started_at: new Date().toISOString(),
          phases: Object.fromEntries(
            PHASE_ORDER.map(p => [p, { status: 'pending' as const, started_at: null, completed_at: null }])
          ),
          current_phase: 'discovery',
          overall_status: 'pending',
        });
      }
      setError(null);
    } catch {
      setError('Unable to connect to backend. Pipeline may still be running.');
    } finally {
      setLoading(false);
    }
  }, [businessId]);

  useEffect(() => {
    fetchProgress();
    const interval = setInterval(fetchProgress, 5000);
    return () => clearInterval(interval);
  }, [fetchProgress]);

  const isComplete = progress?.overall_status === 'completed';

  return (
    <Box maxWidth="600px" mx="auto">
      <Card size="2">
        <Flex direction="column" gap="3">
          <Text size="4" weight="bold">Onboarding Pipeline</Text>
          <Text size="2" color="gray">
            {isComplete
              ? 'All phases completed successfully!'
              : 'Tracking pipeline execution status...'}
          </Text>

          {error && (
            <Card variant="surface">
              <Text size="2" color="orange">{error}</Text>
            </Card>
          )}

          {PHASE_ORDER.map((phase, index) => {
            const phaseData = progress?.phases[phase];
            const status = phaseData?.status || 'pending';
            const isCurrent = progress?.current_phase === phase;

            return (
              <Card
                key={phase}
                variant={isCurrent ? 'classic' : 'surface'}
                size="1"
                style={{
                  borderLeft: `4px solid ${
                    status === 'completed' ? '#4CAF50' :
                    status === 'in_progress' ? '#2196F3' :
                    status === 'failed' ? '#f44336' :
                    '#666'
                  }`,
                }}
              >
                <Flex justify="between" align="center">
                  <Flex gap="3" align="center">
                    <Flex
                      align="center"
                      justify="center"
                      style={{
                        width: 28,
                        height: 28,
                        borderRadius: '50%',
                        background: status === 'completed' ? '#4CAF50' :
                                    status === 'in_progress' ? '#2196F3' :
                                    status === 'failed' ? '#f44336' : '#444',
                        color: '#fff',
                        fontSize: 14,
                        fontWeight: 'bold',
                      }}
                    >
                      {status === 'completed' ? <CheckCircledIcon /> :
                       status === 'failed' ? <CrossCircledIcon /> :
                       status === 'in_progress' ? <ReloadIcon /> :
                       index + 1}
                    </Flex>
                    <Flex direction="column">
                      <Text size="2" weight="medium">{PHASE_LABELS[phase]}</Text>
                      <Text size="1" color="gray">{PHASE_DESCRIPTIONS[phase]}</Text>
                    </Flex>
                  </Flex>
                  <StatusBadge status={status} />
                </Flex>
                {phaseData?.details && (
                  <Text size="1" color="gray" style={{ marginTop: 4, marginLeft: 40 }}>
                    {phaseData.details}
                  </Text>
                )}
              </Card>
            );
          })}

          {progress && (
            <Card variant="surface" size="1">
              <Flex justify="center" align="center" gap="2">
                <Text size="2" color="gray">Overall:</Text>
                <Text size="2" weight="bold"
                  color={isComplete ? 'green' : progress.overall_status === 'has_failures' ? 'red' : 'blue'}
                >
                  {progress.overall_status.toUpperCase().replace('_', ' ')}
                </Text>
              </Flex>
            </Card>
          )}

          <Flex gap="2" justify="end">
            <Button variant="surface" type="button" onClick={onBack}>Back</Button>
            <Button
              variant="soft"
              type="button"
              onClick={fetchProgress}
              disabled={loading}
            >
              <ReloadIcon /> Refresh
            </Button>
            <Button type="button" onClick={onFinish} disabled={!isComplete}>
              {isComplete ? 'Open Dashboard' : 'Waiting...'}
            </Button>
          </Flex>
        </Flex>
      </Card>
    </Box>
  );
};

export default OnboardingProgress;
