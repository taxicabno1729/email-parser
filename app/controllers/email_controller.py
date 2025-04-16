import os
import json
import pandas as pd
from datetime import datetime
from utils.email_connector import EmailConnector
from utils.email_parser import EmailParser

class EmailController:
    def __init__(self):
        self.connector = None
        self.parser = EmailParser()
        self.export_directory = os.path.join(os.getcwd(), 'exports')
        
        # Create exports directory if it doesn't exist
        if not os.path.exists(self.export_directory):
            os.makedirs(self.export_directory)
    
    def connect(self, server, port, email, password):
        """
        Connect to email server
        """
        self.connector = EmailConnector(server, port, email, password)
        return self.connector.connect()
    
    def disconnect(self):
        """
        Disconnect from email server
        """
        if self.connector:
            return self.connector.disconnect()
        return "Not connected"
    
    def fetch_emails(self, folder="INBOX", limit=10, criteria="ALL"):
        """
        Fetch emails from specified folder
        """
        if not self.connector or not self.connector.connection:
            # Try to connect using environment variables
            try:
                server = os.getenv('EMAIL_SERVER')
                port = os.getenv('EMAIL_PORT')
                email = os.getenv('EMAIL_USER')
                password = os.getenv('EMAIL_PASSWORD')
                
                if server and port and email and password:
                    self.connect(server, port, email, password)
                else:
                    raise Exception("No active connection and missing environment variables")
            except Exception as e:
                raise Exception(f"Connection failed: {str(e)}")
        
        return self.connector.fetch_emails(folder, limit, criteria)
    
    def parse_email(self, email_content):
        """
        Parse email content
        """
        return self.parser.parse(email_content)
    
    def batch_process(self, emails):
        """
        Process multiple emails
        """
        results = []
        
        for email in emails:
            parsed_data = self.parser.parse(email['body'])
            
            # Add metadata
            parsed_data['email_id'] = email['id']
            parsed_data['email_subject'] = email['subject']
            parsed_data['email_from'] = email['from']
            parsed_data['email_date'] = email['date']
            
            results.append(parsed_data)
        
        return results
    
    def export_data(self, data, format_type='csv'):
        """
        Export parsed data to a file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"email_data_{timestamp}"
        
        if format_type == 'json':
            file_path = os.path.join(self.export_directory, f"{filename}.json")
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            return file_path
        
        elif format_type == 'csv':
            file_path = os.path.join(self.export_directory, f"{filename}.csv")
            
            # Convert to DataFrame for CSV export
            # If data is a list of dictionaries, convert directly
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                # Flatten nested dictionaries for CSV format
                flattened_data = []
                
                for item in data:
                    flat_item = {}
                    
                    for key, value in item.items():
                        if isinstance(value, dict):
                            for subkey, subvalue in value.items():
                                flat_item[f"{key}_{subkey}"] = subvalue
                        elif isinstance(value, list) and key == 'items':
                            # Special handling for item lists
                            for i, subitem in enumerate(value):
                                for subkey, subvalue in subitem.items():
                                    flat_item[f"item{i+1}_{subkey}"] = subvalue
                        else:
                            flat_item[key] = value
                    
                    flattened_data.append(flat_item)
                
                df = pd.DataFrame(flattened_data)
            else:
                # If it's a single dictionary, convert to a single-row DataFrame
                df = pd.DataFrame([data])
            
            df.to_csv(file_path, index=False)
            return file_path
        
        elif format_type == 'excel':
            file_path = os.path.join(self.export_directory, f"{filename}.xlsx")
            
            # Similar logic as CSV but for Excel
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                flattened_data = []
                
                for item in data:
                    flat_item = {}
                    
                    for key, value in item.items():
                        if isinstance(value, dict):
                            for subkey, subvalue in value.items():
                                flat_item[f"{key}_{subkey}"] = subvalue
                        elif isinstance(value, list) and key == 'items':
                            for i, subitem in enumerate(value):
                                for subkey, subvalue in subitem.items():
                                    flat_item[f"item{i+1}_{subkey}"] = subvalue
                        else:
                            flat_item[key] = value
                    
                    flattened_data.append(flat_item)
                
                df = pd.DataFrame(flattened_data)
            else:
                df = pd.DataFrame([data])
            
            df.to_excel(file_path, index=False)
            return file_path
        
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def get_email_statistics(self, emails):
        """
        Generate statistics from processed emails
        """
        if not emails:
            return {}
        
        total_emails = len(emails)
        
        # Count emails by sender
        senders = {}
        for email in emails:
            sender = email.get('email_from', '')
            if sender:
                senders[sender] = senders.get(sender, 0) + 1
        
        # Find most common vendor
        vendors = {}
        for email in emails:
            vendor = email.get('vendor_name', '')
            if vendor:
                vendors[vendor] = vendors.get(vendor, 0) + 1
        
        # Calculate average order total
        order_totals = []
        for email in emails:
            total = email.get('total_amount', '')
            if total:
                try:
                    # Clean up amount string and convert to float
                    cleaned_total = total.replace('$', '').replace(',', '')
                    order_totals.append(float(cleaned_total))
                except ValueError:
                    pass
        
        avg_order_total = sum(order_totals) / len(order_totals) if order_totals else 0
        
        return {
            'total_emails': total_emails,
            'sender_distribution': senders,
            'top_vendors': vendors,
            'average_order_total': avg_order_total
        } 