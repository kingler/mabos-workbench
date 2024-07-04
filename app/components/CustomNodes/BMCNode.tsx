import React from 'react';
import { Handle, Position } from 'reactflow';

interface BMCNodeProps {
  data: {
    label: string;
    category: string;
    content: string;
  };
}

const BMCNode: React.FC<BMCNodeProps> = ({ data }) => {
  return (
    <div className={`bmc-node ${data.category}`}>
      <Handle type="target" position={Position.Top} />
      <div className="bmc-node-content">
        <h3>{data.label}</h3>
        <p>{data.content}</p>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default BMCNode;
