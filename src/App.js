import React, { useState } from 'react';
import EmailParser from './components/EmailParser';
import ResultsDisplay from './components/ResultsDisplay';
import { parseEmailContent } from './utils/parser';

function App() {
  const [parsedData, setParsedData] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const handleParse = (emailContent) => {
    setLoading(true);
    
    // Simulate async processing
    setTimeout(() => {
      const results = parseEmailContent(emailContent);
      setParsedData(results);
      setLoading(false);
    }, 500);
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Purchase Order Email Parser</h1>
          <p className="mt-2 text-lg text-gray-600">Extract key information from purchase order emails</p>
        </div>
        
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <EmailParser onParse={handleParse} loading={loading} />
          
          {parsedData && (
            <ResultsDisplay data={parsedData} />
          )}
        </div>
      </div>
    </div>
  );
}

export default App; 