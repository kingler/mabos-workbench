import React from 'react'
import { Handle, Position } from 'reactflow'

const PlanNode = ({ data }) => {
  return (
    <div className="plan-node">
      <Handle type="target" position={Position.Top} />
      <div className="plan-content">
        <h3>{data.label}</h3>
        <p>Steps: {data.steps.join(', ')}</p>
        <p>Status: {data.status}</p>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  )
}

export default PlanNode