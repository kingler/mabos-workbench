// src/components/CustomNodes/UMLNode.tsx
import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

const UMLNode = ({ data }: NodeProps) => {
  return (
    <div className="uml-node">
      <Handle type="target" position={Position.Top} />
      <div>{data.label}</div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default UMLNode;