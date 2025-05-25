import React from 'react';
import dynamic from 'next/dynamic';

// Dynamically import the DiagramEditor component to avoid SSR issues with ReactFlow
const DiagramEditor = dynamic(() => import('./DiagramEditor'), { ssr: false });

const Workbench: React.FC = () => {
  return (
    <div>
      <h1>TOGAF Modeling Workbench</h1>
      <DiagramEditor />
    </div>
  );
};

export default Workbench;