import React, { useState } from 'react';

const EmailParser = ({ onParse, loading }) => {
  const [emailContent, setEmailContent] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (emailContent.trim()) {
      onParse(emailContent);
    }
  };
  
  const handleSampleData = () => {
    const sampleEmail = `
Purchase Order #PO-12345
From: office@acmesupplies.com
Date: May 14, 2023

VENDOR: TechComponents Inc.
SHIPPING ADDRESS: 123 Business Park, Suite 400, San Francisco, CA 94107

ITEMS:
1. Premium SSD Drive 500GB
   Quantity: 5
   Unit Cost: $89.99
   Total: $449.95

2. Wireless Keyboard MK-7
   Quantity: 10
   Unit Cost: $45.50
   Total: $455.00

SUMMARY:
Subtotal: $904.95
Shipping: $24.99
Tax (8.5%): $76.92
Total: $1,006.86

SHIPPING INFORMATION:
Carrier: FedEx
Tracking Number: FX-78901234567
Estimated Delivery: May 20, 2023
`;
    setEmailContent(sampleEmail);
  };

  return (
    <div className="px-6 py-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-gray-800">Email Content</h2>
        <button
          type="button"
          onClick={handleSampleData}
          className="text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          Load Sample Data
        </button>
      </div>
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <textarea
            className="w-full h-64 px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Paste purchase order email content here..."
            value={emailContent}
            onChange={(e) => setEmailContent(e.target.value)}
          ></textarea>
        </div>
        
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={loading || !emailContent.trim()}
            className={`px-4 py-2 font-medium rounded-md ${
              loading || !emailContent.trim()
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {loading ? 'Processing...' : 'Parse Email'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default EmailParser; 