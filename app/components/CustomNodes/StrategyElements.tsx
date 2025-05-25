import React from 'react';
import { Handle, Position } from 'reactflow';

const baseStyle: React.CSSProperties = {
  padding: '10px',
  borderRadius: '5px',
  border: '1px solid black',
  textAlign: 'center',
  backgroundColor: '#fffacd'
};

const ResourceNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Resource</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const CapabilityNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Capability</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const ValueStreamNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Value Stream</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const CourseOfActionNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Course of Action</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

export { ResourceNode, CapabilityNode, ValueStreamNode, CourseOfActionNode };