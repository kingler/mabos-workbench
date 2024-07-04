'use client'

import React, { useState, useEffect } from 'react'

const OnboardingAgent: React.FC = () => {
  const [step, setStep] = useState(0)
  const [isVisible, setIsVisible] = useState(true)

  const steps = [
    "Welcome to the Business-Oriented MAS Development Platform!",
    "Let's start by creating a Business Model Canvas.",
    "Now, let's define some goals for your business.",
    "Great! Let's create some agents to achieve these goals.",
    "Finally, let's set up the environment for your agents.",
    "You're all set! Feel free to explore the platform."
  ]

  useEffect(() => {
    if (step < steps.length - 1) {
      const timer = setTimeout(() => setStep(step + 1), 5000)
      return () => clearTimeout(timer)
    }
  }, [step, steps.length])

  if (!isVisible) return null

  return (
    <div className="onboarding-agent fixed bottom-4 right-4 bg-white p-4 rounded shadow-lg">
      <p>{steps[step]}</p>
      {step === steps.length - 1 && (
        <button 
          onClick={() => setIsVisible(false)}
          className="mt-2 p-2 bg-blue-500 text-white rounded"
        >
          Got it!
        </button>
      )}
    </div>
  )
}

export default OnboardingAgent