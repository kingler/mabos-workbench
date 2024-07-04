import React from 'react';
import { getBezierPath, Position } from 'reactflow';

interface AccessEdgeProps {
  id: string;
  sourceX: number;
  sourceY: number;
  targetX: number;
  targetY: number;
  sourcePosition: Position;
  targetPosition: Position;
  style?: React.CSSProperties;
  markerEnd?: string;
}

const AccessEdge = ({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition, style = {}, markerEnd }: AccessEdgeProps) => {
  const [edgePath] = getBezierPath({
    sourceX,
    sourceY,
    targetX,
    targetY,
    sourcePosition,
    targetPosition,
  });

  return (
    <>
      <path id={id} style={style} className="react-flow__edge-path" d={edgePath} markerEnd={markerEnd} />
      <text>
        <textPath href={`#${id}`} style={{ fontSize: 12 }} startOffset="50%" textAnchor="middle">
          Access
        </textPath>
      </text>
    </>
  );
};

export default AccessEdge;