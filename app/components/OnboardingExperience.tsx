import React, { useState } from 'react'
import '@radix-ui/themes/styles.css';
import * as Dialog from '@radix-ui/react-dialog'
import { Cross2Icon } from '@radix-ui/react-icons'
import { Box, Flex, IconButton, Text } from '@radix-ui/themes'
import WelcomeScreen from './onboarding/WelcomeScreen'
import BusinessOverview from './onboarding/BusinessOverview'
import ModelSelection from './onboarding/ModelSelection'
import FinalStep from './onboarding/FinalStep'



const OnboardingExperience: React.FC<{ isOpen: boolean; onClose: () => void }> = ({ isOpen, onClose }) => {
  const [step, setStep] = useState(0)
  const [businessData, setBusinessData] = useState({
    name: '',
    industry: '',
    description: '',
    type: '',
    businessModel: {},
    goals: [],
  })

  const updateBusinessData = (data: Partial<typeof businessData>) => {
    setBusinessData(prevData => ({ ...prevData, ...data }))
  }

  const nextStep = () => setStep(prevStep => prevStep + 1)
  const prevStep = () => setStep(prevStep => prevStep - 1)

  const renderStep = () => {
    switch (step) {
      case 0:
        return <WelcomeScreen onStart={nextStep} />
      case 1:
        return (
          <BusinessOverview
            data={businessData}
            updateData={updateBusinessData}
            onNext={nextStep}
          />
        )
      case 2:
        return (
          <BusinessModelCanvas
            data={businessData.businessModel}
            updateData={(data) => updateBusinessData({ businessModel: data })}
            onNext={nextStep}
            onBack={prevStep}
          />
        )
      case 3:
        return (
          <GoalHierarchy
            data={businessData.goals}
            updateData={(data) => updateBusinessData({ goals: data })}
            onNext={nextStep}
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
              <Text size="5" weight="bold">Onboarding</Text>
            </Dialog.Title>
            <Dialog.Description asChild>
              <Text size="2" color="gray">Let's get you started with our platform.</Text>
            </Dialog.Description>
          </Box>
          
          {/* Your step content here */}
          {step === 0 && <WelcomeScreen onNext={() => setStep(1)} />}
          {step === 1 && <BusinessOverview onNext={() => setStep(2)} onBack={() => setStep(0)} />}
          {step === 2 && <ModelSelection onNext={() => setStep(3)} onBack={() => setStep(1)} />}
          {step === 3 && <FinalStep onFinish={onClose} onBack={() => setStep(2)} />}

          <Dialog.Close asChild>
            <IconButton variant="ghost" color="gray" position="absolute" top="2" right="2">
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