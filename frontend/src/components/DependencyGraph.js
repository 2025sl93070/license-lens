import React from 'react';
import ReactFlow, { Background, Controls } from 'reactflow';
import 'reactflow/dist/style.css';
 
const statusColors = {
  OK: '#d4edda',
  REVIEW: '#fff3cd',
  FLAGGED: '#f8d7da',
  UNKNOWN: '#e2e3e5',
};
 
function DependencyGraph({ data }) {
  const nodes = data.results.map((dep, index) => ({
    id: `${index}`,
    position: { x: index * 200, y: 100 },
    data: { label: `${dep.name}\n${dep.license}` },
    style: {
      background: statusColors[dep.status] || statusColors.UNKNOWN,
      border: '1px solid #ccc',
      borderRadius: '8px',
      padding: '10px',
      fontSize: '12px',
      width: 150,
    },
  }));
 
  const edges = data.results.slice(1).map((dep, index) => ({
    id: `e${index}-${index + 1}`,
    source: `${index}`,
    target: `${index + 1}`,
  }));
 
  return (
<div style={{ width: '100%', height: '400px', marginTop: '20px' }}>
<h3>Dependency Tree</h3>
<ReactFlow nodes={nodes} edges={edges} fitView>
<Background />
<Controls />
</ReactFlow>
</div>
  );
}
 
export default DependencyGraph;