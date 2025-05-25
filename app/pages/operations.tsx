import React from 'react';
import ArchitecturalView from '../components/ArchitecturalView';

const OperationsPage: React.FC = () => {
  return (
    <div>
      <h1>Operations View</h1>
      <ArchitecturalView viewName="operations_view" />
    </div>
  );
};

export default OperationsPage;