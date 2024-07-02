import React from 'react';
import { Box, Heading, Text, Button } from '@radix-ui/themes';

const OnboardingExperience = () => {
  return (
    <Box className="onboarding p-4 bg-gray-900 text-white">
      <Heading size="4" className="mb-4">Welcome to Our Platform</Heading>
      <Text className="mb-4">Let's get you started with a quick tour.</Text>
      <Button variant="solid">Start Tour</Button>
    </Box>
  );
};

export default OnboardingExperience;
