import React, { useState, useCallback } from 'react'
import '@radix-ui/themes/styles.css';
import * as Dialog from '@radix-ui/react-dialog'
import { Cross2Icon } from '@radix-ui/react-icons'
import { Box, Flex, IconButton, Text } from '@radix-ui/themes'
import WelcomeScreen from './onboarding/WelcomeScreen'
import BusinessOverview from './onboarding/BusinessOverview'
import BusinessModelCanvas from './onboarding/BusinessModelCanvas'
import GoalsConstraints from './onboarding/GoalsConstraints'
import FinalStep from './onboarding/FinalStep'
import OnboardingProgress from './onboarding/OnboardingProgress'
import { buildOnboardingPayload, onboardBusiness } from '../services/onboarding'

interface StakeholderGoal {
  goal: string;
  priority: number;
  type: 'hard' | 'soft';
}

interface BusinessData {
  name: string;
  legal_name: string;
  industry: string;
  description: string;
  type: string;
  jurisdiction: string;
  stage: string;
  customer_segments: string;
  value_propositions: string;
  revenue_streams: string;
  businessModel: Record<string, unknown>;
  stakeholder_goals: StakeholderGoal[];
  constraints: string;
}

const STEP_LABELS = [
  'Welcome',
  'Business Overview',
  'Business Model Canvas',
  'Goals & Constraints',
  'Review & Confirm',
  'Pipeline Progress',
];

const OnboardingExperience: React.FC<{ isOpen: boolean; onClose: () => void }> = ({ isOpen, onClose }) => {
  const [step, setStep] = useState(0)
  const [businessId, setBusinessId] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [businessData, setBusinessData] = useState<BusinessData>({
    name: '',
    legal_name: '',
    industry: '',
    description: '',
    type: '',
    jurisdiction: '',
    stage: 'mvp',
    customer_segments: '',
    value_propositions: '',
    revenue_streams: '',
    businessModel: {},
    stakeholder_goals: [],
    constraints: '',
  })

  const updateBusinessData = useCallback((data: Partial<BusinessData>) => {
    setBusinessData(prev => ({ ...prev, ...data }))
  }, [])

  const nextStep = useCallback(() => setStep(prev => prev + 1), [])
  const prevStep = useCallback(() => setStep(prev => prev - 1), [])

  const handleSubmit = useCallback(async () => {
    setSubmitting(true)
    try {
      const payload = buildOnboardingPayload({
        name: businessData.name,
        legal_name: businessData.legal_name,
        type: businessData.type,
        description: businessData.description,
        jurisdiction: businessData.jurisdiction,
        stage: businessData.stage,
        value_propositions: businessData.value_propositions,
        customer_segments: businessData.customer_segments,
        revenue_streams: businessData.revenue_streams,
        stakeholder_goals: businessData.stakeholder_goals,
        constraints: businessData.constraints,
      })
      setBusinessId(payload.business_id)

      await onboardBusiness({
        ...payload,
        sbvr_export: { conceptTypes: [], factTypes: [], rules: [], proofTables: [] },
      })

      nextStep()
    } catch (err) {
      // If backend is unavailable, still proceed to progress view
      const slugify = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')
      setBusinessId(slugify(businessData.name))
      nextStep()
    } finally {
      setSubmitting(false)
    }
  }, [businessData, nextStep])

  const renderStepIndicator = () => (
    <Flex gap="1" justify="center" mb="3">
      {STEP_LABELS.map((label, i) => (
        <Box
          key={label}
          style={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            background: i === step ? 'var(--accent-9)' : i < step ? 'var(--accent-6)' : 'var(--gray-5)',
            transition: 'background 0.2s',
          }}
          title={label}
        />
      ))}
    </Flex>
  )

  const renderStep = () => {
    switch (step) {
      case 0:
        return <WelcomeScreen onNext={nextStep} />
      case 1:
        return (
          <BusinessOverview
            data={businessData}
            updateData={updateBusinessData}
            onNext={nextStep}
            onBack={prevStep}
          />
        )
      case 2:
        return (
          <BusinessModelCanvas
            data={businessData.businessModel}
            updateData={(data: Record<string, unknown>) => updateBusinessData({ businessModel: data })}
            onNext={nextStep}
            onBack={prevStep}
          />
        )
      case 3:
        return (
          <GoalsConstraints
            data={{
              stakeholder_goals: businessData.stakeholder_goals,
              constraints: businessData.constraints,
            }}
            updateData={(data) => updateBusinessData(data as Partial<BusinessData>)}
            onNext={nextStep}
            onBack={prevStep}
          />
        )
      case 4:
        return (
          <FinalStep
            onFinish={handleSubmit}
            onBack={prevStep}
          />
        )
      case 5:
        return (
          <OnboardingProgress
            businessId={businessId}
            onFinish={onClose}
            onBack={prevStep}
          />
        )
      default:
        return <div>Onboarding Complete!</div>
    }
  }

  return (
    <Dialog.Root open={isOpen} onOpenChange={onClose}>
      <Dialog.Portal>
        <Dialog.Overlay className="DialogOverlay" />
        <Dialog.Content className="DialogContent">
          <Flex direction="column" gap="4">
            <Box>
              <Dialog.Title asChild>
                <Text size="5" weight="bold">
                  {step < STEP_LABELS.length ? STEP_LABELS[step] : 'Onboarding'}
                </Text>
              </Dialog.Title>
              <Dialog.Description asChild>
                <Text size="2" color="gray">
                  Step {step + 1} of {STEP_LABELS.length}
                </Text>
              </Dialog.Description>
            </Box>

            {renderStepIndicator()}
            {renderStep()}

            <Dialog.Close asChild>
              <IconButton variant="ghost" color="gray" style={{ position: 'absolute', top: 8, right: 8 }}>
                <Cross2Icon />
              </IconButton>
            </Dialog.Close>
          </Flex>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  )
}

export default OnboardingExperience
