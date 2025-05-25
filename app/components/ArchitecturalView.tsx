import React, { useState, useEffect } from 'react';
import ReactFlow, { MiniMap, Controls, Background, Elements } from 'react-flow-renderer';
import { fetchViewModel } from '../services/api';

interface ArchitecturalViewProps {
  viewName: string;
}

const transformElements = (data: any) => {
  const nodes = data.elements.map((element: any) => ({
    id: element.id,
    data: { label: element.name },
    position: { x: Math.random() * 400, y: Math.random() * 400 },
  }));

  const edges = data.relationships.map((rel: any) => ({
    id: `${rel.source}-${rel.target}`,
    source: rel.source,
    target: rel.target,
    type: 'default',
    label: rel.relationship_type,
  }));

  return [...nodes, ...edges];
};

const ArchitecturalView: React.FC<ArchitecturalViewProps> = ({ viewName }) => {
  const [elements, setElements] = useState<Elements>([]);

  useEffect(() => {
    fetchViewModel(viewName).then((data: any) => {
      const transformedElements = transformElements(data);
      setElements(transformedElements);
    });
  }, [viewName]);

  return (
    <div style={{ height: '100vh' }}>
      <ReactFlow elements={elements} style={{ width: '100%', height: '100%' }}>
        <MiniMap />
        <Controls />
        <Background />
      </ReactFlow>
    </div>
  );
};

export default ArchitecturalView;