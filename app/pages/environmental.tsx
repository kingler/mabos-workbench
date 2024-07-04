import React from 'react';
import ArchitecturalView from '../components/ArchitecturalView';

const EnvironmentalPage: React.FC = () => {
  return (
    <div>
      <h1>Environmental View</h1>
      <ArchitecturalView viewName="environmental_view" />
    </div>
  );
};

export default EnvironmentalPage;