import React from 'react';
import { Handle, Position } from 'reactflow';

interface ActionNodeData {
  label: string;
  effect: string;
}

const ActionNode = ({ data }: { data: ActionNodeData }) => {
  return (
    <div className="action-node">
      <Handle type="target" position={Position.Top} />
      <div className="action-content">
        <h3>{data.label}</h3>
        <p>Effect: {data.effect}</p>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default ActionNode;