import React from 'react';
import { useForm, Controller, useFieldArray } from 'react-hook-form';
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
  Box,
  IconButton,
} from '@radix-ui/themes';
import { PlusIcon, Cross2Icon } from '@radix-ui/react-icons';

interface Goal {
  goal: string;
  priority: number;
  type: 'hard' | 'soft';
}

interface GoalsConstraintsData {
  stakeholder_goals: Goal[];
  constraints: string;
}

interface GoalsConstraintsProps {
  data?: Partial<GoalsConstraintsData>;
  updateData?: (data: Partial<GoalsConstraintsData>) => void;
  onNext: () => void;
  onBack: () => void;
}

const GoalsConstraints: React.FC<GoalsConstraintsProps> = ({ data, updateData, onNext, onBack }) => {
  const { control, handleSubmit } = useForm<GoalsConstraintsData>({
    defaultValues: {
      stakeholder_goals: data?.stakeholder_goals || [
        { goal: '', priority: 0.8, type: 'hard' },
      ],
      constraints: data?.constraints || '',
    },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'stakeholder_goals',
  });

  const onSubmit = (formData: GoalsConstraintsData) => {
    updateData?.(formData);
    onNext();
  };

  return (
    <Box maxWidth="600px" mx="auto">
      <Card size="2">
        <Form.Root onSubmit={handleSubmit(onSubmit)}>
          <Flex direction="column" gap="3">
            <Text size="4" weight="bold">Goals & Constraints</Text>
            <Text size="2" color="gray">
              Define your top business goals and any constraints the system should respect.
            </Text>

            <Text size="3" weight="medium">Stakeholder Goals</Text>

            {fields.map((field, index) => (
              <Card key={field.id} variant="surface" size="1">
                <Flex direction="column" gap="2">
                  <Flex justify="between" align="center">
                    <Text size="2" weight="medium">Goal {index + 1}</Text>
                    {fields.length > 1 && (
                      <IconButton
                        variant="ghost"
                        color="red"
                        size="1"
                        type="button"
                        onClick={() => remove(index)}
                      >
                        <Cross2Icon />
                      </IconButton>
                    )}
                  </Flex>

                  <Controller
                    name={`stakeholder_goals.${index}.goal`}
                    control={control}
                    rules={{ required: true }}
                    render={({ field: f }) => (
                      <TextField.Root>
                        <TextField.Input {...f} placeholder="e.g., Reach $1M ARR within 12 months" />
                      </TextField.Root>
                    )}
                  />

                  <Grid columns="2" gap="2">
                    <Flex direction="column" gap="1">
                      <Text size="1" color="gray">Priority (0-1)</Text>
                      <Controller
                        name={`stakeholder_goals.${index}.priority`}
                        control={control}
                        render={({ field: f }) => (
                          <TextField.Root>
                            <TextField.Input
                              {...f}
                              type="number"
                              min="0"
                              max="1"
                              step="0.1"
                              onChange={(e) => f.onChange(parseFloat(e.target.value) || 0)}
                            />
                          </TextField.Root>
                        )}
                      />
                    </Flex>

                    <Flex direction="column" gap="1">
                      <Text size="1" color="gray">Type</Text>
                      <Controller
                        name={`stakeholder_goals.${index}.type`}
                        control={control}
                        render={({ field: f }) => (
                          <Select.Root onValueChange={f.onChange} value={f.value}>
                            <Select.Trigger />
                            <Select.Content>
                              <Select.Item value="hard">Hard (must achieve)</Select.Item>
                              <Select.Item value="soft">Soft (nice to have)</Select.Item>
                            </Select.Content>
                          </Select.Root>
                        )}
                      />
                    </Flex>
                  </Grid>
                </Flex>
              </Card>
            ))}

            {fields.length < 5 && (
              <Button
                variant="soft"
                type="button"
                onClick={() => append({ goal: '', priority: 0.5, type: 'soft' })}
              >
                <PlusIcon /> Add Goal
              </Button>
            )}

            <Text size="3" weight="medium">Constraints</Text>
            <Controller
              name="constraints"
              control={control}
              render={({ field }) => (
                <TextArea
                  {...field}
                  placeholder="One per line: e.g.,&#10;Budget: $50k initial&#10;Timeline: Launch in 3 months&#10;Must comply with GDPR"
                  rows={4}
                />
              )}
            />

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

export default GoalsConstraints;
