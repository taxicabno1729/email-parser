/**
 * Extracts purchase order information from email content
 * @param {string} emailContent - The email content to parse
 * @returns {Object} Parsed purchase order data
 */
export const parseEmailContent = (emailContent) => {
  // Initialize result object
  const result = {
    vendorName: '',
    items: [],
    shipping: '',
    trackingNumber: '',
    taxes: '',
    total: '',
  };

  // Extract vendor name
  const vendorMatch = emailContent.match(/VENDOR:\s*(.*)/i);
  if (vendorMatch && vendorMatch[1]) {
    result.vendorName = vendorMatch[1].trim();
  }

  // Extract tracking number
  const trackingMatch = emailContent.match(/Tracking Number:\s*([\w-]+)/i);
  if (trackingMatch && trackingMatch[1]) {
    result.trackingNumber = trackingMatch[1].trim();
  }

  // Extract shipping cost
  const shippingMatch = emailContent.match(/Shipping:\s*(\$[\d.,]+)/i);
  if (shippingMatch && shippingMatch[1]) {
    result.shipping = shippingMatch[1].trim();
  }

  // Extract taxes
  const taxMatch = emailContent.match(/Tax.*?:\s*(\$[\d.,]+)/i);
  if (taxMatch && taxMatch[1]) {
    result.taxes = taxMatch[1].trim();
  }

  // Extract total
  const totalMatch = emailContent.match(/Total:\s*(\$[\d.,]+)/i);
  if (totalMatch && totalMatch[1]) {
    result.total = totalMatch[1].trim();
  }

  // Extract items
  // This is a bit more complex as we need to find all items with their details
  try {
    // Find the items section
    const itemsSection = emailContent.match(/ITEMS:([\s\S]*?)(?=SUMMARY:|SHIPPING INFORMATION:|$)/i);
    
    if (itemsSection && itemsSection[1]) {
      const itemsText = itemsSection[1].trim();
      
      // Split by numbered items (1., 2., etc.)
      const itemBlocks = itemsText.split(/\d+\.\s+/).filter(Boolean);
      
      result.items = itemBlocks.map(block => {
        const name = block.split('\n')[0].trim();
        
        const quantityMatch = block.match(/Quantity:\s*(\d+)/i);
        const quantity = quantityMatch ? quantityMatch[1] : '';
        
        const unitCostMatch = block.match(/Unit Cost:\s*(\$[\d.,]+)/i);
        const unitCost = unitCostMatch ? unitCostMatch[1] : '';
        
        const totalMatch = block.match(/Total:\s*(\$[\d.,]+)/i);
        const total = totalMatch ? totalMatch[1] : '';
        
        return {
          name,
          quantity,
          unitCost,
          total
        };
      });
    }
  } catch (error) {
    console.error('Error parsing items:', error);
  }

  return result;
};

/**
 * Takes a string that might contain a price and ensures it's in a consistent format
 * @param {string} priceStr - String containing a price
 * @returns {string} Formatted price string
 */
export const formatPrice = (priceStr) => {
  if (!priceStr) return '';
  
  // Remove any non-numeric characters except for decimal point
  const numericValue = priceStr.replace(/[^\d.]/g, '');
  
  // Format as currency
  return `$${parseFloat(numericValue).toFixed(2)}`;
}; 