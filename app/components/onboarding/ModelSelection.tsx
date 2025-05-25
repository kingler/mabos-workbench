import React from 'react';
import { Box, Flex, Text, Heading, Button, Card, RadioGroup } from '@radix-ui/themes';

interface ModelSelectionProps {
  onNext: () => void;
  onBack: () => void;
  selectedModel: string;
  setSelectedModel: (model: string) => void;
}

const ModelSelection: React.FC<ModelSelectionProps> = ({ onNext, onBack, selectedModel, setSelectedModel }) => {
  return (
    <Box maxWidth="500px" mx="auto">
      <Card size="3">
        <Flex direction="column" gap="4">
          <Heading size="5">Select a Business Model</Heading>
          <Text size="2">Choose the type of model you want to create for your business:</Text>
          
          <RadioGroup.Root value={selectedModel} onValueChange={setSelectedModel}>
            <Flex direction="column" gap="2">
              <Text as="label" size="2">
                <Flex gap="2">
                  <RadioGroup.Item value="BMC" /> Business Model Canvas
                </Flex>
              </Text>
              <Text as="label" size="2">
                <Flex gap="2">
                  <RadioGroup.Item value="BMM" /> Business Motivation Model
                </Flex>
              </Text>
              <Text as="label" size="2">
                <Flex gap="2">
                  <RadioGroup.Item value="BPMN" /> Business Process Model and Notation
                </Flex>
              </Text>
              <Text as="label" size="2">
                <Flex gap="2">
                  <RadioGroup.Item value="AOM" /> Agent-Oriented Model
                </Flex>
              </Text>
            </Flex>
          </RadioGroup.Root>
          
          <Flex justify="between" mt="4">
            <Button onClick={onBack} variant="surface">Back</Button>
            <Button onClick={onNext}>Next</Button>
          </Flex>
        </Flex>
      </Card>
    </Box>
  );
};

export default ModelSelection;
