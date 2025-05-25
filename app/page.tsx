import React from 'react';
import dynamic from 'next/dynamic';

// Dynamically import the Workbench component to avoid SSR issues
const Workbench = dynamic(() => import('../components/Workbench'), { ssr: false });

const MainPage: React.FC = () => {
  return (
    <div>
      <h1>TOGAF Modeling Workbench</h1>
      <Workbench />
    </div>
  );
};

export default MainPage;