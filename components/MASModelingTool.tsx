import React from 'react';
import { Box, Heading, Flex, Text } from '@radix-ui/themes';

const MASModelingTool = () => {
  return (
    <Box className="mas-modeling-tool p-4 bg-gray-900 text-white">
      <Heading size="4" className="mb-4">MAS Modeling Tool</Heading>
      <Flex direction="column" gap="2">
        <Box className="p-2 bg-gray-800 rounded">
          <Text>Agent Definition</Text>
        </Box>
        <Box className="p-2 bg-gray-800 rounded">
          <Text>Environment Setup</Text>
        </Box>
        <Box className="p-2 bg-gray-800 rounded">
          <Text>Interaction Rules</Text>
        </Box>
      </Flex>
    </Box>
  );
};

export default MASModelingTool;
