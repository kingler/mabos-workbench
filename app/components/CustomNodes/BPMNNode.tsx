import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

const BPMNNode: React.FC<NodeProps> = ({ data }) => {
  return (
    <div className="bpmn-node">
      <Handle type="target" position={Position.Top} />
      <div className="bpmn-content">
        <div className="bpmn-type">{data.type}</div>
        <div className="bpmn-label">{data.label}</div>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default BPMNNode;
