import re
from bs4 import BeautifulSoup
import json

class EmailParser:
    def __init__(self):
        self.patterns = {
            'order_number': r'Order\s*(?:Number|#)[:\s]*([A-Za-z0-9\-]+)',
            'order_date': r'Order\s*Date[:\s]*([A-Za-z0-9,\s]+)',
            'total_amount': r'(?:Order\s*Total|Total)[:\s]*[$€£]?([0-9,.]+)',
            'shipping_address': r'(?:Shipping|Delivery)\s*Address[:\s]*(.*?)(?=\n\n|\n[A-Z]|\Z)',
            'tracking_number': r'(?:Tracking\s*(?:Number|#)|Track\s*Your\s*Package)[:\s]*([A-Za-z0-9]+)',
            'vendor_name': r'(?:From|Vendor|Seller)[:\s]*([A-Za-z0-9\s,.]+)(?=\n|<)',
            'email_from': r'From:[:\s]*([A-Za-z0-9\s,.@<>]+)'
        }
    
    def parse(self, email_content):
        """
        Parse email content and extract structured data
        """
        # Try to determine if the content is HTML
        if re.search(r'<html.*?>|<body.*?>', email_content, re.IGNORECASE):
            return self.parse_html(email_content)
        else:
            return self.parse_text(email_content)
    
    def parse_html(self, html_content):
        """
        Parse HTML email content
        """
        # Convert HTML to plain text first
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text(' ', strip=True)
        
        # Extract basic information using patterns
        extracted_data = self._extract_patterns(text_content)
        
        # Try to extract tables from HTML for items
        tables = soup.find_all('table')
        items = []
        
        for table in tables:
            if self._is_likely_items_table(table):
                items = self._extract_items_from_table(table)
                if items:
                    break
        
        if items:
            extracted_data['items'] = items
        
        return extracted_data
    
    def parse_text(self, text_content):
        """
        Parse plain text email content
        """
        # Extract data using patterns
        extracted_data = self._extract_patterns(text_content)
        
        # Try to extract items from text using pattern recognition
        items = self._extract_items_from_text(text_content)
        
        if items:
            extracted_data['items'] = items
            
        return extracted_data
    
    def _extract_patterns(self, text):
        """
        Extract structured data using regex patterns
        """
        extracted_data = {}
        
        for key, pattern in self.patterns.items():
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                extracted_data[key] = match.group(1).strip()
        
        return extracted_data
    
    def _is_likely_items_table(self, table):
        """
        Identify if a table is likely to contain order items
        """
        text = table.get_text().lower()
        
        # Check if table contains these keywords
        item_indicators = ['item', 'product', 'description', 'quantity', 'price', 'amount', 'subtotal']
        score = sum(1 for indicator in item_indicators if indicator in text)
        
        return score >= 3  # If at least 3 indicators are present
    
    def _extract_items_from_table(self, table):
        """
        Extract items from an HTML table
        """
        items = []
        rows = table.find_all('tr')
        
        # Skip header row
        if len(rows) < 2:
            return []
        
        # Try to determine the column indices
        header_cells = rows[0].find_all(['th', 'td'])
        header_text = [cell.get_text().strip().lower() for cell in header_cells]
        
        # Map column indices
        column_map = {}
        for i, text in enumerate(header_text):
            if 'item' in text or 'product' in text or 'description' in text:
                column_map['name'] = i
            elif 'qty' in text or 'quantity' in text:
                column_map['quantity'] = i
            elif 'price' in text or 'unit' in text or 'cost' in text:
                column_map['price'] = i
            elif 'total' in text or 'amount' in text or 'subtotal' in text:
                column_map['total'] = i
        
        # If we couldn't determine the columns, return empty
        if 'name' not in column_map:
            return []
        
        # Extract items from rows
        for row in rows[1:]:
            cells = row.find_all(['td', 'th'])
            if len(cells) < max(column_map.values()) + 1:
                continue
                
            item = {}
            
            if 'name' in column_map:
                item['name'] = cells[column_map['name']].get_text().strip()
                
            if 'quantity' in column_map:
                qty_text = cells[column_map['quantity']].get_text().strip()
                qty_match = re.search(r'(\d+)', qty_text)
                if qty_match:
                    item['quantity'] = int(qty_match.group(1))
            
            if 'price' in column_map:
                price_text = cells[column_map['price']].get_text().strip()
                price_match = re.search(r'[\$€£]?([0-9,.]+)', price_text)
                if price_match:
                    item['unit_price'] = price_match.group(1)
            
            if 'total' in column_map:
                total_text = cells[column_map['total']].get_text().strip()
                total_match = re.search(r'[\$€£]?([0-9,.]+)', total_text)
                if total_match:
                    item['total_price'] = total_match.group(1)
            
            # Only add non-empty items
            if item and 'name' in item and item['name']:
                items.append(item)
        
        return items
    
    def _extract_items_from_text(self, text):
        """
        Extract items from plain text
        """
        items = []
        
        # Look for item patterns in text
        # This is a simplified approach and may need customization based on email formats
        item_pattern = r'(\d+)\s*x\s*([^,\n]+)[\s,]*(?:\$|EUR|£)?([0-9,.]+)'
        
        matches = re.finditer(item_pattern, text)
        
        for match in matches:
            quantity = int(match.group(1))
            name = match.group(2).strip()
            price = match.group(3).strip()
            
            item = {
                'name': name,
                'quantity': quantity,
                'unit_price': price
            }
            
            items.append(item)
        
        return items 