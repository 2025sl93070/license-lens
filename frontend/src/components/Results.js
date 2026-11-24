import React from 'react';
 
const statusColors = {
  OK: { background: '#d4edda', color: '#155724' },
  REVIEW: { background: '#fff3cd', color: '#856404' },
  FLAGGED: { background: '#f8d7da', color: '#721c24' },
  UNKNOWN: { background: '#e2e3e5', color: '#383d41' },
};
 
function Results({ data }) {
  const handleDownload = () => {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `licenselens-report.json`;
    link.click();
    URL.revokeObjectURL(url);
  };
 
  return (
<div>
<h2>Analysis Results</h2>
<p>File: {data.filename}</p>
<p>Total Dependencies: {data.total_dependencies}</p>
 
      <button onClick={handleDownload}>
        Download Report (JSON)
</button>
 
      <table border="1" cellPadding="8" style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
<thead>
<tr>
<th>Package</th>
<th>Version</th>
<th>License</th>
<th>Status</th>
<th>Reason</th>
</tr>
</thead>
<tbody>
          {data.results.map((dep, index) => (
<tr key={index}>
<td>{dep.name}</td>
<td>{dep.version}</td>
<td>{dep.license}</td>
<td>
<span style={{
                  padding: '4px 8px',
                  borderRadius: '4px',
                  ...statusColors[dep.status] || statusColors.UNKNOWN
                }}>
                  {dep.status}
</span>
</td>
<td>{dep.reason}</td>
</tr>
          ))}
</tbody>
</table>
</div>
  );
}
 
export default Results;