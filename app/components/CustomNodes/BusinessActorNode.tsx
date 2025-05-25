import React from 'react';
import { Handle, Position } from 'reactflow';

interface BusinessActorNodeProps {
  data: {
    label: string;
  };
}

const BusinessActorNode = ({ data }: BusinessActorNodeProps) => {
  return (
    <div className="business-actor-node">
      <Handle type="target" position={Position.Top} />
      <div className="node-content">
        <div className="node-icon">👤</div>
        <div className="node-label">{data.label}</div>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default BusinessActorNode;