import React from 'react';
import { Handle, Position } from 'reactflow';

const baseStyle: React.CSSProperties = {
  padding: '10px',
  borderRadius: '5px',
  border: '1px solid black',
  textAlign: 'center',
  backgroundColor: '#98fb98'
};

const NodeNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Node</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const DeviceNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Device</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const SystemSoftwareNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>System Software</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const TechnologyCollaborationNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Technology Collaboration</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const TechnologyInterfaceNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Technology Interface</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const PathNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Path</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const CommunicationNetworkNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Communication Network</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const TechnologyFunctionNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Technology Function</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const TechnologyProcessNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Technology Process</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const TechnologyInteractionNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Technology Interaction</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const TechnologyEventNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Technology Event</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const TechnologyServiceNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Technology Service</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const ArtifactNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Artifact</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

export { NodeNode, DeviceNode, SystemSoftwareNode, TechnologyCollaborationNode, TechnologyInterfaceNode, PathNode, CommunicationNetworkNode, TechnologyFunctionNode, TechnologyProcessNode, TechnologyInteractionNode, TechnologyEventNode, TechnologyServiceNode, ArtifactNode };