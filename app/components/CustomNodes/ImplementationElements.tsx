import React from 'react';
import { Handle, Position } from 'reactflow';

const baseStyle: React.CSSProperties = {
  padding: '10px',
  borderRadius: '5px',
  border: '1px solid black',
  textAlign: 'center',
  backgroundColor: '#f08080'
};

const WorkPackageNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Work Package</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const DeliverableNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Deliverable</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const ImplementationEventNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Implementation Event</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const PlateauNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Plateau</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const GapNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Gap</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

export { WorkPackageNode, DeliverableNode, ImplementationEventNode, PlateauNode, GapNode };