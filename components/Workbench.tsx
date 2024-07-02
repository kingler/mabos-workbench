import React from 'react';
import { Box, Heading, Text } from '@radix-ui/themes';

const Workbench = () => {
  return (
    <Box className="workbench p-4 bg-gray-900 text-gray-100">
      <Heading size="4" className="mb-4 text-gray-100">Workbench</Heading>
      <Text>Your workbench content goes here</Text>
    </Box>
  );
};

export default Workbench;
