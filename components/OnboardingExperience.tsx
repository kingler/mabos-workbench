import React from 'react';
import { Box, Heading, Text, Button } from '@radix-ui/themes';

const OnboardingExperience = () => {
  return (
    <Box className="onboarding p-4 bg-gray-900 text-gray-100">
      <Heading size="4" className="mb-4 text-gray-100">Welcome to Our Platform</Heading>
      <Text className="mb-4">Let's get you started with a quick tour.</Text>
      <Button variant="solid" className="bg-indigo-600 hover:bg-indigo-700 transition-colors">Start Tour</Button>
    </Box>
  );
};

export default OnboardingExperience;
