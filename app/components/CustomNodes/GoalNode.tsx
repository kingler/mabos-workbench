import React from 'react';
import { Handle, Position } from 'reactflow';

const GoalNode = ({ data }) => {
  return (
    <div className="goal-node">
      <Handle type="target" position={Position.Top} />
      <div className="goal-content">
        <h3>{data.label}</h3>
        <p>Priority: {data.priority}</p>
        <p>Status: {data.status}</p>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default GoalNode;