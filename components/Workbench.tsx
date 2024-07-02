import React from 'react';
import { Box, Heading, Text } from '@radix-ui/themes';

const Workbench = () => {
  return (
    <Box className="workbench p-4 bg-gray-900 text-white">
      <Heading size="4" className="mb-4">Workbench</Heading>
      <Text>Your workbench content goes here</Text>
    </Box>
  );
};

export default Workbench;
