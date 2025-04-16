import React from 'react';

const ResultsDisplay = ({ data }) => {
  const { 
    vendorName, 
    items, 
    shipping, 
    trackingNumber, 
    taxes, 
    total 
  } = data;

  return (
    <div className="bg-gray-50 px-6 py-6 border-t border-gray-200">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Extracted Information</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="font-medium text-gray-700 mb-2">Vendor Information</h3>
          <p className="text-gray-800">{vendorName}</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="font-medium text-gray-700 mb-2">Shipping Information</h3>
          <p className="text-gray-800">Cost: {shipping}</p>
          <p className="text-gray-800">Tracking Number: {trackingNumber}</p>
        </div>
      </div>
      
      <div className="mt-6 bg-white p-4 rounded-lg shadow">
        <h3 className="font-medium text-gray-700 mb-2">Order Items</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Item</th>
                <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantity</th>
                <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Unit Cost</th>
                <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {items.map((item, index) => (
                <tr key={index}>
                  <td className="px-3 py-2 whitespace-nowrap text-sm text-gray-900">{item.name}</td>
                  <td className="px-3 py-2 whitespace-nowrap text-sm text-gray-900">{item.quantity}</td>
                  <td className="px-3 py-2 whitespace-nowrap text-sm text-gray-900">{item.unitCost}</td>
                  <td className="px-3 py-2 whitespace-nowrap text-sm text-gray-900">{item.total}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      
      <div className="mt-6 bg-white p-4 rounded-lg shadow">
        <h3 className="font-medium text-gray-700 mb-2">Order Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          <div>
            <p className="text-gray-600">Taxes:</p>
            <p className="text-gray-800 font-medium">{taxes}</p>
          </div>
          <div>
            <p className="text-gray-600">Total Amount:</p>
            <p className="text-gray-800 font-medium">{total}</p>
          </div>
        </div>
      </div>
      
      <div className="mt-6 flex justify-end">
        <button
          type="button"
          onClick={() => navigator.clipboard.writeText(JSON.stringify(data, null, 2))}
          className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
        >
          Copy as JSON
        </button>
      </div>
    </div>
  );
};

export default ResultsDisplay; 