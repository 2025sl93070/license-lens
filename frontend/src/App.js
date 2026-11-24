import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import Results from './components/Results';
import DependencyGraph from './components/DependencyGraph';
import './App.css';
 
function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
 
  return (
<div className="App">
<h1>LicenseLens</h1>
<p>Analyze your project dependencies and understand their licenses.</p>
<FileUpload
        setResults={setResults}
        setLoading={setLoading}
        setError={setError}
      />
      {loading && <p>Analyzing dependencies...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {results && (
<>
<Results data={results} />
<DependencyGraph data={results} />
</>
      )}
</div>
  );
}
 
export default App;