import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import {
  Box,
  Card,
  Flex,
  Grid,
  Text,
  TextArea,
  Button,
  Accordion,
  TextField,
  Heading,
  ScrollArea
} from '@radix-ui/themes';

interface BusinessModelCanvasProps {
  data: {
    keyPartners: string;
    keyActivities: string;
    keyResources: string;
    valuePropositions: {
      customerJobs: string;
      pains: string;
      gains: string;
      products: string;
      painRelievers: string;
      gainCreators: string;
    };
    customerRelationships: string;
    channels: string;
    customerSegments: string;
    costStructure: string;
    revenueStreams: string;
  };
  updateData: (data: Partial<BusinessModelCanvasProps['data']>) => void;
  onNext: () => void;
  onBack: () => void;
}

const BusinessModelCanvas: React.FC<BusinessModelCanvasProps> = ({ data, updateData, onNext, onBack }) => {
  const { control, handleSubmit } = useForm({ defaultValues: data });

  const onSubmit = (formData: BusinessModelCanvasProps['data']) => {
    updateData(formData);
    onNext();
  };

  const renderCanvasBlock = (title: string, name: string, description: string) => (
    <Accordion.Item value={name}>
      <Accordion.Trigger>{title}</Accordion.Trigger>
      <Accordion.Content>
        <Text size="2" mb="2">{description}</Text>
        <Controller
          name={name}
          control={control}
          render={({ field }) => (
            <TextArea placeholder={`Enter ${title}...`} {...field} />
          )}
        />
      </Accordion.Content>
    </Accordion.Item>
  );

  const renderValueProposition = () => (
    <Accordion.Item value="valuePropositions">
      <Accordion.Trigger>Value Propositions</Accordion.Trigger>
      <Accordion.Content>
        <Grid columns="2" gap="2">
          <Box>
            <Heading size="3" mb="2">Customer Profile</Heading>
            <Controller
              name="valuePropositions.customerJobs"
              control={control}
              render={({ field }) => (
                <TextArea placeholder="Customer Jobs..." {...field} mb="2" />
              )}
            />
            <Controller
              name="valuePropositions.pains"
              control={control}
              render={({ field }) => (
                <TextArea placeholder="Customer Pains..." {...field} mb="2" />
              )}
            />
            <Controller
              name="valuePropositions.gains"
              control={control}
              render={({ field }) => (
                <TextArea placeholder="Customer Gains..." {...field} />
              )}
            />
          </Box>
          <Box>
            <Heading size="3" mb="2">Value Map</Heading>
            <Controller
              name="valuePropositions.products"
              control={control}
              render={({ field }) => (
                <TextArea placeholder="Products & Services..." {...field} mb="2" />
              )}
            />
            <Controller
              name="valuePropositions.painRelievers"
              control={control}
              render={({ field }) => (
                <TextArea placeholder="Pain Relievers..." {...field} mb="2" />
              )}
            />
            <Controller
              name="valuePropositions.gainCreators"
              control={control}
              render={({ field }) => (
                <TextArea placeholder="Gain Creators..." {...field} />
              )}
            />
          </Box>
        </Grid>
      </Accordion.Content>
    </Accordion.Item>
  );

  return (
    <Box maxWidth="800px" mx="auto">
      <Card size="2">
        <ScrollArea scrollbars="vertical" style={{ height: '70vh' }}>
          <Heading size="4" mb="4">Business Model Canvas</Heading>
          <form onSubmit={handleSubmit(onSubmit)}>
            <Accordion type="multiple">
              {renderCanvasBlock('Key Partners', 'keyPartners', 'Who are your key partners and suppliers?')}
              {renderCanvasBlock('Key Activities', 'keyActivities', 'What key activities does your value proposition require?')}
              {renderCanvasBlock('Key Resources', 'keyResources', 'What key resources does your value proposition require?')}
              {renderValueProposition()}
              {renderCanvasBlock('Customer Relationships', 'customerRelationships', 'What type of relationship does each customer segment expect?')}
              {renderCanvasBlock('Channels', 'channels', 'Through which channels do your customer segments want to be reached?')}
              {renderCanvasBlock('Customer Segments', 'customerSegments', 'For whom are you creating value? Who are your most important customers?')}
              {renderCanvasBlock('Cost Structure', 'costStructure', 'What are the most important costs inherent in your business model?')}
              {renderCanvasBlock('Revenue Streams', 'revenueStreams', 'For what value are your customers really willing to pay?')}
            </Accordion>
            <Flex justify="between" mt="4">
              <Button onClick={onBack} variant="surface">Back</Button>
              <Button type="submit">Next</Button>
            </Flex>
          </form>
        </ScrollArea>
      </Card>
    </Box>
  );
};

export default BusinessModelCanvas;