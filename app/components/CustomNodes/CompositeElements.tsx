import React from 'react';
import { Handle, Position } from 'reactflow';

const baseStyle: React.CSSProperties = {
  padding: '10px',
  borderRadius: '5px',
  border: '1px solid black',
  textAlign: 'center',
  backgroundColor: '#ffdead'
};

const GroupingNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Grouping</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const LocationNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Location</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

export { GroupingNode, LocationNode };