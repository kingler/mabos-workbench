'use client'

import React, { useState, useCallback } from 'react'
import ReactFlow, { 
  Node, 
  Edge, 
  Controls, 
  Background, 
  useNodesState, 
  useEdgesState,
  NodeTypes
} from 'reactflow'
import 'reactflow/dist/style.css'
import { OpenAI } from 'openai'

// Import custom node components
import AOMNode from './CustomNodes/AOMNode'
import AOPNNode from './CustomNodes/AOPNNode'
import BMCNode from './CustomNodes/BMCNode'
import BMMNode from './CustomNodes/BMMNode'
import BPMNNode from './CustomNodes/BPMNNode'
import UMLNode from './CustomNodes/UMLNode'

// Define model types
type ModelType = 'AOM' | 'BMC' | 'BMM' | 'BPMN' | 'UML'

// Define node types
const nodeTypes: NodeTypes = {
  aomNode: AOMNode,
  bmcNode: BMCNode,
  bmmNode: BMMNode,
  bpmnNode: BPMNNode,
  umlNode: UMLNode,
}

const BusinessModelGenerator: React.FC = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])
  const [businessDescription, setBusinessDescription] = useState('')
  const [selectedModel, setSelectedModel] = useState<ModelType>('BMC')

  const generateModel = useCallback(async () => {
    try {
      const openai = new OpenAI({
        apiKey: process.env.NEXT_PUBLIC_OPENAI_API_KEY,
        dangerouslyAllowBrowser: true
      });

      const response = await openai.chat.completions.create({
        model: "gpt-4",
        messages: [
          {
            role: "system",
            content: `You are an AI assistant that generates ${selectedModel} based on business descriptions. Output should be in a JSON format that can be easily converted to nodes and edges for ReactFlow. Each node should have a type corresponding to the model type (e.g., 'aomNode', 'bmcNode', etc.) and appropriate data fields.`
          },
          {
            role: "user",
            content: `Generate a ${selectedModel} for the following business description: ${businessDescription}`
          }
        ],
      })

      const generatedModel = JSON.parse(response.choices[0].message.content || '{}')

      // Convert generated model to nodes and edges
      const newNodes: Node[] = generatedModel.nodes.map((node: any, index: number) => ({
        id: index.toString(),
        type: node.type, // This should match the nodeTypes keys (e.g., 'aomNode', 'bmcNode', etc.)
        position: { x: node.x, y: node.y },
        data: { ...node.data },
      }))

      const newEdges: Edge[] = generatedModel.edges.map((edge: any, index: number) => ({
        id: `e${index}`,
        source: edge.source.toString(),
        target: edge.target.toString(),
      }))

      setNodes(newNodes)
      setEdges(newEdges)
    } catch (error) {
      console.error('Error generating model:', error)
    }
  }, [businessDescription, selectedModel, setNodes, setEdges])

  return (
    <div style={{ height: '100vh', width: '100%' }}>
      <div style={{ padding: '20px' }}>
        <textarea
          value={businessDescription}
          onChange={(e) => setBusinessDescription(e.target.value)}
          placeholder="Enter business description"
          style={{ width: '100%', height: '100px' }}
        />
        <select
          value={selectedModel}
          onChange={(e) => setSelectedModel(e.target.value as ModelType)}
          style={{ marginLeft: '10px' }}
        >
          <option value="AOM">Agent-Oriented Model</option>
          <option value="BMC">Business Model Canvas</option>
          <option value="BMM">Business Motivation Model</option>
          <option value="BPMN">Business Process Model Notation</option>
          <option value="UML">Unified Modeling Language</option>
        </select>
        <button onClick={generateModel} style={{ marginLeft: '10px' }}>Generate Model</button>
      </div>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodeTypes={nodeTypes}
      >
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  )
}

export default BusinessModelGenerator