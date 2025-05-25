import React from 'react';
import { Handle, Position } from 'reactflow';

const baseStyle: React.CSSProperties = {
  padding: '10px',
  borderRadius: '5px',
  border: '1px solid black',
  textAlign: 'center',
  backgroundColor: '#e6e6fa'
};

const StakeholderNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Stakeholder</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const DriverNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Driver</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const AssessmentNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Assessment</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const GoalNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Goal</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const OutcomeNode: React.FC = () => (
  <div style={baseStyle}>
    <Handle type="target" position={Position.Top} />
    <div>Outcome</div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

export { StakeholderNode, DriverNode, AssessmentNode, GoalNode, OutcomeNode };