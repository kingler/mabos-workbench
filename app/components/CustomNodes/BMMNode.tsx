import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

const BMMNode: React.FC<NodeProps> = ({ data }) => {
  return (
    <div className="bmm-node">
      <Handle type="target" position={Position.Top} />
      <div className="bmm-content">
        <div className="bmm-type">{data.type}</div>
        <div className="bmm-name">{data.name}</div>
        <div className="bmm-description">{data.description}</div>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default BMMNode;
