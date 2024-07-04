import React from 'react';
import { Box, Heading, Flex, Text, Button } from '@radix-ui/themes';

const ModelTransformation = () => {
  return (
    <Box className="model-transformation p-4 bg-gray-900 text-gray-100">
      <Heading size="4" className="mb-4 text-gray-100">Model Transformation</Heading>
      <Flex direction="column" gap="4">
        <Box className="p-2 bg-gray-800 rounded hover:bg-gray-700 transition-colors">
          <Text>Source Model</Text>
        </Box>
        <Button variant="solid" className="bg-indigo-600 hover:bg-indigo-700 transition-colors">Transform</Button>
        <Box className="p-2 bg-gray-800 rounded hover:bg-gray-700 transition-colors">
          <Text>Target Model</Text>
        </Box>
      </Flex>
    </Box>
  );
};

export default ModelTransformation;
