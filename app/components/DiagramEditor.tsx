import React, { useCallback } from 'react';
import ReactFlow, { useNodesState, useEdgesState, addEdge, MiniMap, Controls, Background, Node, Connection } from 'reactflow';
import 'reactflow/dist/style.css';
import { StakeholderNode, DriverNode, AssessmentNode, GoalNode, OutcomeNode } from './CustomNodes/MotivationElements';
import { ResourceNode, CapabilityNode, ValueStreamNode, CourseOfActionNode } from './CustomNodes/StrategyElements';
import { BusinessActorNode, BusinessRoleNode, BusinessCollaborationNode, BusinessInterfaceNode, BusinessProcessNode } from './CustomNodes/BusinessLayerElements';
import { ApplicationComponentNode, ApplicationCollaborationNode, ApplicationInterfaceNode, ApplicationFunctionNode, ApplicationInteractionNode, ApplicationProcessNode, ApplicationEventNode, ApplicationServiceNode, DataObjectNode } from './CustomNodes/ApplicationElements';
import { NodeNode, DeviceNode, SystemSoftwareNode, TechnologyCollaborationNode, TechnologyInterfaceNode, PathNode, CommunicationNetworkNode, TechnologyFunctionNode, TechnologyProcessNode, TechnologyInteractionNode, TechnologyEventNode, TechnologyServiceNode, ArtifactNode } from './CustomNodes/TechnologyElements';
import { EquipmentNode, FacilityNode, DistributionNetworkNode, MaterialNode } from './CustomNodes/PhysicalElements';
import { WorkPackageNode, DeliverableNode, ImplementationEventNode, PlateauNode, GapNode } from './CustomNodes/ImplementationElements';
import { GroupingNode, LocationNode } from './CustomNodes/CompositeElements';

const nodeTypes = {
  stakeholder: StakeholderNode,
  driver: DriverNode,
  assessment: AssessmentNode,
  goal: GoalNode,
  outcome: OutcomeNode,
  resource: ResourceNode,
  capability: CapabilityNode,
  valueStream: ValueStreamNode,
  courseOfAction: CourseOfActionNode,
  businessActor: BusinessActorNode,
  businessRole: BusinessRoleNode,
  businessCollaboration: BusinessCollaborationNode,
  businessInterface: BusinessInterfaceNode,
  businessProcess: BusinessProcessNode,
  applicationComponent: ApplicationComponentNode,
  applicationCollaboration: ApplicationCollaborationNode,
  applicationInterface: ApplicationInterfaceNode,
  applicationFunction: ApplicationFunctionNode,
  applicationInteraction: ApplicationInteractionNode,
  applicationProcess: ApplicationProcessNode,
  applicationEvent: ApplicationEventNode,
  applicationService: ApplicationServiceNode,
  dataObject: DataObjectNode,
  node: NodeNode,
  device: DeviceNode,
  systemSoftware: SystemSoftwareNode,
  technologyCollaboration: TechnologyCollaborationNode,
  technologyInterface: TechnologyInterfaceNode,
  path: PathNode,
  communicationNetwork: CommunicationNetworkNode,
  technologyFunction: TechnologyFunctionNode,
  technologyProcess: TechnologyProcessNode,
  technologyInteraction: TechnologyInteractionNode,
  technologyEvent: TechnologyEventNode,
  technologyService: TechnologyServiceNode,
  artifact: ArtifactNode,
  equipment: EquipmentNode,
  facility: FacilityNode,
  distributionNetwork: DistributionNetworkNode,
  material: MaterialNode,
  workPackage: WorkPackageNode,
  deliverable: DeliverableNode,
  implementationEvent: ImplementationEventNode,
  plateau: PlateauNode,
  gap: GapNode,
  grouping: GroupingNode,
  location: LocationNode
};

const initialNodes: Node[] = [
  { id: '1', type: 'stakeholder', position: { x: 100, y: 50 }, data: { label: 'Stakeholder' } },
  { id: '2', type: 'driver', position: { x: 250, y: 50 }, data: { label: 'Driver' } },
  // Add more initial nodes as needed
];

const DiagramEditor: React.FC = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  const onConnect = useCallback((params: Connection) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  return (
    <div style={{ height: '90vh' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        style={{ width: '100%', height: '100%' }}
      >
        <MiniMap />
        <Controls />
        <Background />
      </ReactFlow>
    </div>
  );
};

export default DiagramEditor;