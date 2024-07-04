import React from 'react';
import { Handle, Position } from 'reactflow';

interface AgentNodeData {
  label: string;
  goals: string[];
  beliefs: string[];
}

const AgentNode = ({ data }: { data: AgentNodeData }) => {
  return (
    <div className="agent-node">
      <Handle type="target" position={Position.Top} />
      <div className="agent-content">
        <h3>{data.label}</h3>
        <p>Goals: {data.goals.join(', ')}</p>
        <p>Beliefs: {data.beliefs.join(', ')}</p>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default AgentNode;

export default AgentNode;