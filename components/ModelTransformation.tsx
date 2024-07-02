import React from 'react';
import { Box, Heading, Flex, Text, Button } from '@radix-ui/themes';

const ModelTransformation = () => {
  return (
    <Box className="model-transformation p-4 bg-gray-900 text-white">
      <Heading size="4" className="mb-4">Model Transformation</Heading>
      <Flex direction="column" gap="4">
        <Box className="p-2 bg-gray-800 rounded">
          <Text>Source Model</Text>
        </Box>
        <Button variant="solid">Transform</Button>
        <Box className="p-2 bg-gray-800 rounded">
          <Text>Target Model</Text>
        </Box>
      </Flex>
    </Box>
  );
};

export default ModelTransformation;
