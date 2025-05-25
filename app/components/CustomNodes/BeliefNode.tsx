import React from 'react'
import { Handle, Position } from 'reactflow'

const BeliefNode = ({ data }) => {
  return (
    <div className="belief-node">
      <Handle type="target" position={Position.Top} />
      <div className="belief-content">
        <h3>{data.label}</h3>
        <p>Certainty: {data.certainty}</p>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  )
}

export default BeliefNode