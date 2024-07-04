import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface AOPNData {
  id: string;
  beliefs: string[];
  desires: string[];
  intentions: string[];
  goals: { id: string; description: string; subgoals: string[] }[];
  plans: { id: string; description: string; actions: string[] }[];
  role: string;
}

const AOPNNode: React.FC<NodeProps<AOPNData>> = ({ data }) => {
  return (
    <div className="aopn-node">
      <Handle type="target" position={Position.Top} />
      <div className="aopn-content">
        <div className="aopn-id">Agent: {data.id}</div>
        <div className="aopn-role">Role: {data.role}</div>
        <div className="aopn-section">
          <h4>Beliefs:</h4>
          <ul>
            {data.beliefs.map((belief, index) => (
              <li key={index}>{belief}</li>
            ))}
          </ul>
        </div>
        <div className="aopn-section">
          <h4>Desires:</h4>
          <ul>
            {data.desires.map((desire, index) => (
              <li key={index}>{desire}</li>
            ))}
          </ul>
        </div>
        <div className="aopn-section">
          <h4>Intentions:</h4>
          <ul>
            {data.intentions.map((intention, index) => (
              <li key={index}>{intention}</li>
            ))}
          </ul>
        </div>
        <div className="aopn-section">
          <h4>Goals:</h4>
          <ul>
            {data.goals.map((goal) => (
              <li key={goal.id}>
                {goal.description}
                {goal.subgoals.length > 0 && (
                  <ul>
                    {goal.subgoals.map((subgoal, index) => (
                      <li key={index}>{subgoal}</li>
                    ))}
                  </ul>
                )}
              </li>
            ))}
          </ul>
        </div>
        <div className="aopn-section">
          <h4>Plans:</h4>
          <ul>
            {data.plans.map((plan) => (
              <li key={plan.id}>
                {plan.description}
                <ul>
                  {plan.actions.map((action, index) => (
                    <li key={index}>{action}</li>
                  ))}
                </ul>
              </li>
            ))}
          </ul>
        </div>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default AOPNNode;
