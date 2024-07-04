import React from 'react';
import { Handle, Position } from 'reactflow';

const baseStyle: React.CSSProperties = {
  padding: '10px',
  borderRadius: '5px',
  border: '1px solid black',
  textAlign: 'center',
  backgroundColor: '#ffffe0'
};

const BusinessActorNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Business Actor</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const BusinessRoleNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Business Role</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const BusinessCollaborationNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Business Collaboration</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const BusinessInterfaceNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Business Interface</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const BusinessProcessNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Business Process</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

export { BusinessActorNode, BusinessRoleNode, BusinessCollaborationNode, BusinessInterfaceNode, BusinessProcessNode };