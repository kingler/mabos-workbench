import React from 'react';
import { Box, Flex, Text, Heading, Button, Card } from '@radix-ui/themes';

interface WelcomeScreenProps {
  onStart: () => void;
}

const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onStart }) => {
  return (
    <Box maxWidth="600px" mx="auto">
      <Card size="3">
        <Flex direction="column" align="center" gap="5">
          <Heading size="7" align="center">
            Welcome to the Goal-Oriented BDI Multi-Agent Business Development Operating System
          </Heading>
          
          <Text size="3" align="center">
            This system will help you model, simulate, and optimize your business using advanced multi-agent technology.
            Let's get started by setting up your business model and defining your goals.
          </Text>
          
          <Flex gap="3">
            <Button size="3" variant="outline" onClick={() => {}}>
              Learn More
            </Button>
            <Button size="3" onClick={onStart}>
              Get Started
            </Button>
          </Flex>
        </Flex>
      </Card>
    </Box>
  );
};

export default WelcomeScreen;