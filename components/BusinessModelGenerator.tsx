import React, { useState } from 'react';
import { Box, Heading, Text, Grid, Flex, Button } from '@radix-ui/themes';

const canvasBlocks = [
  'Key Partners', 'Key Activities', 'Value Propositions', 'Customer Relationships',
  'Customer Segments', 'Key Resources', 'Channels', 'Cost Structure', 'Revenue Streams'
];

const BusinessModelGenerator = () => {
  const [connections, setConnections] = useState<[number, number][]>([]);
  const [selectedBlock, setSelectedBlock] = useState<number | null>(null);

  const handleBlockClick = (index: number) => {
    console.log('Block clicked:', index);
    if (selectedBlock === null) {
      console.log('Selecting block:', index);
      setSelectedBlock(index);
    } else if (selectedBlock !== index) {
      console.log('Creating connection:', selectedBlock, 'to', index);
      setConnections(prev => {
        const newConnections = [...prev, [selectedBlock, index]];
        console.log('New connections:', newConnections);
        return newConnections;
      });
      setSelectedBlock(null);
    } else {
      console.log('Deselecting block:', index);
      setSelectedBlock(null);
    }
  };

  const renderConnections = () => {
    return connections.map(([start, end], index) => (
      <svg key={index} style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none' }}>
        <line x1={`${(start % 3) * 33.33 + 16.67}%`} y1={`${Math.floor(start / 3) * 33.33 + 16.67}%`}
              x2={`${(end % 3) * 33.33 + 16.67}%`} y2={`${Math.floor(end / 3) * 33.33 + 16.67}%`}
              stroke="indigo" strokeWidth="2" strokeDasharray="5,5" />
      </svg>
    ));
  };

  return (
    <Box className="business-model-generator p-4 bg-gray-900 text-gray-100">
      <Heading size="4" className="mb-4 text-gray-100">Business Model Generator</Heading>
      <Box style={{ position: 'relative' }}>
        <Grid columns="3" gap="4">
          {canvasBlocks.map((block, index) => (
            <Box key={index} className={`p-2 bg-gray-800 rounded hover:bg-gray-700 transition-colors cursor-pointer ${selectedBlock === index ? 'ring-2 ring-indigo-500' : ''}`}
                 onClick={() => handleBlockClick(index)}>
              <Text>{block}</Text>
            </Box>
          ))}
        </Grid>
        {renderConnections()}
      </Box>
      <Flex justify="between" mt="4">
        <Button onClick={() => setConnections([])}>Clear Connections</Button>
        <Text>Selected: {selectedBlock !== null ? canvasBlocks[selectedBlock] : 'None'}</Text>
      </Flex>
    </Box>
  );
};

export default BusinessModelGenerator;
