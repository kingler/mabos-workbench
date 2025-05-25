import React from 'react';
import { Box, Flex, Text, Heading, Button, Card } from '@radix-ui/themes';

interface FinalStepProps {
  onFinish: () => void;
  onBack: () => void;
}

const FinalStep: React.FC<FinalStepProps> = ({ onFinish, onBack }) => {
  return (
    <Box maxWidth="500px" mx="auto">
      <Card size="3">
        <Flex direction="column" gap="4">
          <Heading size="5">You're All Set!</Heading>
          <Text size="2">
            Congratulations! You've completed the initial setup for your business model. 
            You're now ready to start using the Goal-Oriented BDI Multi-Agent Business Development Operating System.
          </Text>
          <Text size="2">
            Remember, you can always modify your business model and goals as your business evolves.
          </Text>
          <Flex justify="between" mt="4">
            <Button onClick={onBack} variant="surface">Back</Button>
            <Button onClick={onFinish}>Finish</Button>
          </Flex>
        </Flex>
      </Card>
    </Box>
  );
};

export default FinalStep;
