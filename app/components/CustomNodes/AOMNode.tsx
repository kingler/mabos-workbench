import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface AOMData {
  type: string;
  name: string;
  attributes: string[];
  goals: string[];
  plans: string[];
}

const AOMNode: React.FC<NodeProps<AOMData>> = ({ data }) => {
  return (
    <div className="aom-node">
      <Handle type="target" position={Position.Top} />
      <div className="aom-content">
        <div className="aom-type">{data.type}</div>
        <div className="aom-name">{data.name}</div>
        <div className="aom-section">
          <h4>Attributes:</h4>
          <ul>
            {data.attributes.map((attr: string, index: number) => (
              <li key={index} className="aom-attribute">{attr}</li>
            ))}
          </ul>
        </div>
        <div className="aom-section">
          <h4>Goals:</h4>
          <ul>
            {data.goals.map((goal: string, index: number) => (
              <li key={index} className="aom-goal">{goal}</li>
            ))}
          </ul>
        </div>
        <div className="aom-section">
          <h4>Plans:</h4>
          <ul>
            {data.plans.map((plan: string, index: number) => (
              <li key={index} className="aom-plan">{plan}</li>
            ))}
          </ul>
        </div>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default AOMNode;
