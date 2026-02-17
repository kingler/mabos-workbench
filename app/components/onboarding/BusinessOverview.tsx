import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import {
  Form,
  TextField,
  Select,
  Button,
  Card,
  Flex,
  Grid,
  Text,
  TextArea,
  Box
} from '@radix-ui/themes';

interface BusinessOverviewData {
  name: string;
  legal_name: string;
  industry: string;
  description: string;
  type: string;
  jurisdiction: string;
  stage: string;
  customer_segments: string;
  value_propositions: string;
  revenue_streams: string;
}

interface BusinessOverviewProps {
  data?: Partial<BusinessOverviewData>;
  updateData?: (data: Partial<BusinessOverviewData>) => void;
  onNext: () => void;
  onBack?: () => void;
}

const BusinessOverview: React.FC<BusinessOverviewProps> = ({ data, updateData, onNext, onBack }) => {
  const { control, handleSubmit } = useForm<BusinessOverviewData>({
    defaultValues: {
      name: data?.name || '',
      legal_name: data?.legal_name || '',
      industry: data?.industry || '',
      description: data?.description || '',
      type: data?.type || '',
      jurisdiction: data?.jurisdiction || '',
      stage: data?.stage || 'mvp',
      customer_segments: data?.customer_segments || '',
      value_propositions: data?.value_propositions || '',
      revenue_streams: data?.revenue_streams || '',
    }
  });

  const onSubmit = (formData: BusinessOverviewData) => {
    updateData?.(formData);
    onNext();
  };

  return (
    <Box maxWidth="600px" mx="auto">
      <Card size="2">
        <Form.Root onSubmit={handleSubmit(onSubmit)}>
          <Flex direction="column" gap="3">
            <Text size="4" weight="bold">Business Overview</Text>

            <Form.Field name="name">
              <Form.Label>Business Name</Form.Label>
              <Controller
                name="name"
                control={control}
                rules={{ required: true }}
                render={({ field }) => (
                  <Form.Control asChild>
                    <TextField.Root>
                      <TextField.Input {...field} placeholder="Enter your business name" />
                    </TextField.Root>
                  </Form.Control>
                )}
              />
            </Form.Field>

            <Form.Field name="legal_name">
              <Form.Label>Legal Entity Name</Form.Label>
              <Controller
                name="legal_name"
                control={control}
                render={({ field }) => (
                  <Form.Control asChild>
                    <TextField.Root>
                      <TextField.Input {...field} placeholder="e.g., Acme Corp LLC" />
                    </TextField.Root>
                  </Form.Control>
                )}
              />
            </Form.Field>

            <Form.Field name="type">
              <Form.Label>Business Type</Form.Label>
              <Controller
                name="type"
                control={control}
                rules={{ required: true }}
                render={({ field }) => (
                  <Form.Control asChild>
                    <Select.Root onValueChange={field.onChange} value={field.value}>
                      <Select.Trigger placeholder="Select type..." />
                      <Select.Content>
                        <Select.Item value="ecommerce">E-commerce</Select.Item>
                        <Select.Item value="saas">SaaS</Select.Item>
                        <Select.Item value="consulting">Consulting</Select.Item>
                        <Select.Item value="marketplace">Marketplace</Select.Item>
                        <Select.Item value="retail">Retail</Select.Item>
                        <Select.Item value="other">Other</Select.Item>
                      </Select.Content>
                    </Select.Root>
                  </Form.Control>
                )}
              />
            </Form.Field>

            <Form.Field name="industry">
              <Form.Label>Industry</Form.Label>
              <Controller
                name="industry"
                control={control}
                rules={{ required: true }}
                render={({ field }) => (
                  <Form.Control asChild>
                    <Select.Root onValueChange={field.onChange} value={field.value}>
                      <Select.Trigger placeholder="Select industry..." />
                      <Select.Content>
                        <Select.Item value="technology">Technology</Select.Item>
                        <Select.Item value="finance">Finance</Select.Item>
                        <Select.Item value="healthcare">Healthcare</Select.Item>
                        <Select.Item value="education">Education</Select.Item>
                        <Select.Item value="retail">Retail</Select.Item>
                        <Select.Item value="manufacturing">Manufacturing</Select.Item>
                        <Select.Item value="services">Professional Services</Select.Item>
                        <Select.Item value="other">Other</Select.Item>
                      </Select.Content>
                    </Select.Root>
                  </Form.Control>
                )}
              />
            </Form.Field>

            <Form.Field name="description">
              <Form.Label>Business Description</Form.Label>
              <Controller
                name="description"
                control={control}
                rules={{ required: true }}
                render={({ field }) => (
                  <Form.Control asChild>
                    <TextArea {...field} placeholder="Describe what your business does..." rows={3} />
                  </Form.Control>
                )}
              />
            </Form.Field>

            <Grid columns="2" gap="3">
              <Form.Field name="jurisdiction">
                <Form.Label>Jurisdiction</Form.Label>
                <Controller
                  name="jurisdiction"
                  control={control}
                  render={({ field }) => (
                    <Form.Control asChild>
                      <TextField.Root>
                        <TextField.Input {...field} placeholder="e.g., Delaware, US" />
                      </TextField.Root>
                    </Form.Control>
                  )}
                />
              </Form.Field>

              <Form.Field name="stage">
                <Form.Label>Stage</Form.Label>
                <Controller
                  name="stage"
                  control={control}
                  render={({ field }) => (
                    <Form.Control asChild>
                      <Select.Root onValueChange={field.onChange} value={field.value}>
                        <Select.Trigger />
                        <Select.Content>
                          <Select.Item value="idea">Idea</Select.Item>
                          <Select.Item value="mvp">MVP</Select.Item>
                          <Select.Item value="growth">Growth</Select.Item>
                          <Select.Item value="scale">Scale</Select.Item>
                          <Select.Item value="mature">Mature</Select.Item>
                        </Select.Content>
                      </Select.Root>
                    </Form.Control>
                  )}
                />
              </Form.Field>
            </Grid>

            <Form.Field name="value_propositions">
              <Form.Label>Value Propositions</Form.Label>
              <Controller
                name="value_propositions"
                control={control}
                rules={{ required: true }}
                render={({ field }) => (
                  <Form.Control asChild>
                    <TextArea {...field} placeholder="Comma-separated: e.g., Fast delivery, Low prices, Quality products" rows={2} />
                  </Form.Control>
                )}
              />
            </Form.Field>

            <Form.Field name="customer_segments">
              <Form.Label>Customer Segments</Form.Label>
              <Controller
                name="customer_segments"
                control={control}
                rules={{ required: true }}
                render={({ field }) => (
                  <Form.Control asChild>
                    <TextArea {...field} placeholder="Comma-separated: e.g., SMBs, Enterprise, Consumers" rows={2} />
                  </Form.Control>
                )}
              />
            </Form.Field>

            <Form.Field name="revenue_streams">
              <Form.Label>Revenue Streams</Form.Label>
              <Controller
                name="revenue_streams"
                control={control}
                rules={{ required: true }}
                render={({ field }) => (
                  <Form.Control asChild>
                    <TextArea {...field} placeholder="Comma-separated: e.g., Subscriptions, Transaction fees, Licensing" rows={2} />
                  </Form.Control>
                )}
              />
            </Form.Field>

            <Grid columns="2" gap="2">
              <Button variant="surface" type="button" onClick={onBack}>Back</Button>
              <Button type="submit">Next</Button>
            </Grid>
          </Flex>
        </Form.Root>
      </Card>
    </Box>
  );
};

export default BusinessOverview;
