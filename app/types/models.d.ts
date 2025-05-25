export interface Agent {
  id: string;
  name: string;
  type: string;
  beliefs?: string[];
  desires?: string[];
  intentions?: string[];
}

export interface Ontology {
  // Define the structure of the Ontology type
}

export interface UMLDiagram {
  // Define the structure of the UMLDiagram type
}

export interface SequenceDiagram {
  // Define the structure of the SequenceDiagram type
}

export interface ActivityDiagram {
  // Define the structure of the ActivityDiagram type
}

export interface StateMachineDiagram {
  // Define the structure of the StateMachineDiagram type
}

export interface TOGAFPhase {
  name: string;
  // Add other properties specific to TOGAF phases
}

export interface TOGAFElement {
  // Define the structure of the TOGAFElement type
}

export interface EnterpriseState {
  // Define the structure of the EnterpriseState type
}
