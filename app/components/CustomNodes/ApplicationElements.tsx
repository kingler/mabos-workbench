import React from 'react';
import { Handle, Position } from 'reactflow';

const baseStyle: React.CSSProperties = {
  padding: '10px',
  borderRadius: '5px',
  border: '1px solid black',
  textAlign: 'center',
  backgroundColor: '#b0e0e6'
};

const ApplicationComponentNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Application Component</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const ApplicationCollaborationNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Application Collaboration</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const ApplicationInterfaceNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Application Interface</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const ApplicationFunctionNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Application Function</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const ApplicationInteractionNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Application Interaction</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const ApplicationProcessNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Application Process</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const ApplicationEventNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Application Event</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const ApplicationServiceNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Application Service</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const DataObjectNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Data Object</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

export { ApplicationComponentNode, ApplicationCollaborationNode, ApplicationInterfaceNode, ApplicationFunctionNode, ApplicationInteractionNode, ApplicationProcessNode, ApplicationEventNode, ApplicationServiceNode, DataObjectNode };