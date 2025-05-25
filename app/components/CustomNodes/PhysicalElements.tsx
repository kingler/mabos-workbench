import React from 'react';
import { Handle, Position } from 'reactflow';

const baseStyle: React.CSSProperties = {
  padding: '10px',
  borderRadius: '5px',
  border: '1px solid black',
  textAlign: 'center',
  backgroundColor: '#90ee90'
};

const EquipmentNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Equipment</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const FacilityNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Facility</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const DistributionNetworkNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Distribution Network</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const MaterialNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Material</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

export { EquipmentNode, FacilityNode, DistributionNetworkNode, MaterialNode };