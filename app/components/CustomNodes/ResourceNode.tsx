import React from 'react'
import { Handle, Position } from 'reactflow'

const ResourceNode = ({ data }) => {
  return (
    <div className="resource-node">
      <Handle type="target" position={Position.Top} />
      <div className="resource-content">
        <h3>{data.label}</h3>
        <p>Type: {data.type}</p>
        <p>Availability: {data.availability}</p>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  )
}

export default ResourceNode