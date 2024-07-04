import React from 'react'
import { Handle, Position } from 'reactflow'

interface OrganizationNodeData {
  label: string;
  members: string[];
  norms: string[];
}

const OrganizationNode = ({ data }: { data: OrganizationNodeData }) => {
  return (
    <div className="organization-node">
      <Handle type="target" position={Position.Top} />
      <div className="organization-content">
        <h3>{data.label}</h3>
        <p>Members: {data.members.join(', ')}</p>
        <p>Norms: {data.norms.join(', ')}</p>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  )
}

export default OrganizationNode