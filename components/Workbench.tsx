import React, { useEffect, useState } from 'react';
import { Theme, Box, Container, Heading, Text } from '@radix-ui/themes';
import DiagramEditor from './DiagramEditor';
import { listAgents, createAgent, updateAgent, deleteAgent } from '../services/api';

const Workbench = () => {
  const [agents, setAgents] = useState([]);

  useEffect(() => {
    const fetchAgents = async () => {
      const agentsData = await listAgents();
      setAgents(agentsData);
    };

    fetchAgents();
  }, []);

  const handleCreateAgent = async (agentData) => {
    const newAgent = await createAgent(agentData);
    setAgents([...agents, newAgent]);
  };

  const handleUpdateAgent = async (agentId, agentData) => {
    const updatedAgent = await updateAgent(agentId, agentData);
    setAgents(agents.map(agent => (agent.id === agentId ? updatedAgent : agent)));
  };

  const handleDeleteAgent = async (agentId) => {
    await deleteAgent(agentId);
    setAgents(agents.filter(agent => agent.id !== agentId));
  };

  return (
    <Theme appearance="dark" accentColor="indigo">
      <Box className="workbench">
        <Container size="3">
          <Heading size="5" mb="4">Workbench</Heading>
          <Text>Your workbench content goes here</Text>
          <DiagramEditor 
            agents={agents} 
            onCreateAgent={handleCreateAgent} 
            onUpdateAgent={handleUpdateAgent} 
            onDeleteAgent={handleDeleteAgent} 
          />
        </Container>
      </Box>
    </Theme>
  );
};

export default Workbench;
