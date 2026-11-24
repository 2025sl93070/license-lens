import React, { useState } from 'react';
 
function FileUpload({ setResults, setLoading, setError }) {

  const [file, setFile] = useState(null);
 
  const handleFileChange = (e) => {

    const selected = e.target.files[0];

    if (selected &&

        (selected.name === 'package.json' ||

         selected.name === 'requirements.txt')) {

      setFile(selected);

      setError(null);

    } else {

      setError('Only package.json or requirements.txt files are supported');

      setFile(null);

    }

  };
 
  const handleSubmit = async (e) => {

    e.preventDefault();

    if (!file) {

      setError('Please select a file first');

      return;

    }
 
    const formData = new FormData();

    formData.append('file', file);
 
    try {

      setLoading(true);

      setError(null);

      const response = await fetch('http://localhost:8000/api/v1/analyze', {

        method: 'POST',

        body: formData,

      });
 
      if (!response.ok) {

        throw new Error('Analysis failed. Please try again.');

      }
 
      const data = await response.json();

      setResults(data);

    } catch (err) {

      setError(err.message);

    } finally {

      setLoading(false);

    }

  };
 
  return (
<form onSubmit={handleSubmit}>
<input

        type="file"

        accept=".json,.txt"

        onChange={handleFileChange}

      />
<button type="submit">Analyze</button>
</form>

  );

}
 
export default FileUpload;
 