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

interface BusinessOverviewProps {
  data: {
    name: string;
    industry: string;
    description: string;
    type: string;
  };
  updateData: (data: Partial<BusinessOverviewProps['data']>) => void;
  onNext: () => void;
}

const BusinessOverview: React.FC<BusinessOverviewProps> = ({ data, updateData, onNext }) => {
  const { control, handleSubmit } = useForm({
    defaultValues: data
  });

  const onSubmit = (formData: BusinessOverviewProps['data']) => {
    updateData(formData);
    onNext();
  };

  return (
    <Box maxWidth="500px" mx="auto">
      <Card size="2">
        <Form.Root onSubmit={handleSubmit(onSubmit)}>
          <Flex direction="column" gap="3">
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

            <Form.Field name="industry">
              <Form.Label>Industry</Form.Label>
              <Controller
                name="industry"
                control={control}
                rules={{ required: true }}
                render={({ field }) => (
                  <Form.Control asChild>
                    <Select.Root onValueChange={field.onChange} value={field.value}>
                      <Select.Trigger />
                      <Select.Content>
                        <Select.Item value="technology">Technology</Select.Item>
                        <Select.Item value="finance">Finance</Select.Item>
                        <Select.Item value="healthcare">Healthcare</Select.Item>
                        <Select.Item value="education">Education</Select.Item>
                        <Select.Item value="retail">Retail</Select.Item>
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
                    <TextArea {...field} placeholder="Describe your business..." />
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
                      <Select.Trigger />
                      <Select.Content>
                        <Select.Item value="b2b">B2B</Select.Item>
                        <Select.Item value="b2c">B2C</Select.Item>
                        <Select.Item value="both">Both B2B and B2C</Select.Item>
                      </Select.Content>
                    </Select.Root>
                  </Form.Control>
                )}
              />
            </Form.Field>

            <Grid columns="2" gap="2">
              <Button variant="surface" onClick={() => {}}>Back</Button>
              <Button type="submit">Next</Button>
            </Grid>
          </Flex>
        </Form.Root>
      </Card>
    </Box>
  );
};

export default BusinessOverview;