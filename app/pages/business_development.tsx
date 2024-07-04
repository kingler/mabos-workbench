import React from 'react';
import ArchitecturalView from '../components/ArchitecturalView';

const BusinessDevelopmentPage: React.FC = () => {
  return (
    <div>
      <h1>Business Development View</h1>
      <ArchitecturalView viewName="business_development_view" />
    </div>
  );
};

export default BusinessDevelopmentPage;