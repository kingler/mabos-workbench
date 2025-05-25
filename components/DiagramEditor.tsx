import React from 'react';
import { Box, Heading, Flex } from '@radix-ui/themes';

const DiagramEditor = () => {
  return (
    <Box className="diagram-editor p-4 bg-gray-900 text-gray-100">
      <Heading size="4" className="mb-4 text-gray-100">Diagram Editor</Heading>
      <Flex className="h-96 bg-gray-800 rounded hover:bg-gray-700 transition-colors" justify="center" align="center">
        Diagram Editor Canvas
      </Flex>
    </Box>
  );
};

export default DiagramEditor;
