import React from 'react';
import ArchitecturalView from '../components/ArchitecturalView';

const PerformanceMeasurementPage: React.FC = () => {
  return (
    <div>
      <h1>Performance Measurement View</h1>
      <ArchitecturalView viewName="performance_measurement_view" />
    </div>
  );
};

export default PerformanceMeasurementPage;