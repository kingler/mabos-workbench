import React from 'react';
import { Box, Heading, Text, Grid } from '@radix-ui/themes';

const BusinessModelGenerator = () => {
  return (
    <Box className="business-model-generator p-4 bg-gray-900 text-white">
      <Heading size="4" className="mb-4">Business Model Generator</Heading>
      <Grid columns="3" gap="4">
        {/* Add 9 Box components for the Business Model Canvas */}
        {[...Array(9)].map((_, index) => (
          <Box key={index} className="p-2 bg-gray-800 rounded">
            <Text>Canvas Block {index + 1}</Text>
          </Box>
        ))}
      </Grid>
    </Box>
  );
};

export default BusinessModelGenerator;
