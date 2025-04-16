import imaplib
import email
from email.header import decode_header
import re
import os
from datetime import datetime

class EmailConnector:
    def __init__(self, server, port, email, password):
        self.server = server
        self.port = int(port)
        self.email = email
        self.password = password
        self.connection = None
    
    def connect(self):
        """
        Connect to the email server using IMAP
        """
        try:
            self.connection = imaplib.IMAP4_SSL(self.server, self.port)
            self.connection.login(self.email, self.password)
            return f"Successfully connected to {self.email}"
        except Exception as e:
            raise Exception(f"Connection failed: {str(e)}")
    
    def disconnect(self):
        """
        Disconnect from the email server
        """
        if self.connection:
            try:
                self.connection.logout()
                return "Successfully disconnected"
            except Exception as e:
                raise Exception(f"Disconnect failed: {str(e)}")
        return "No active connection"
    
    def get_folders(self):
        """
        Get list of available folders
        """
        if not self.connection:
            raise Exception("Not connected to server")
        
        folders = []
        response, folder_list = self.connection.list()
        
        if response == 'OK':
            for folder in folder_list:
                folder_name = folder.decode().split('"/"')[-1].strip()
                folders.append(folder_name.replace('"', ''))
        
        return folders
    
    def fetch_emails(self, folder="INBOX", limit=10, criteria="ALL"):
        """
        Fetch emails from specified folder
        """
        if not self.connection:
            raise Exception("Not connected to server")
        
        self.connection.select(folder)
        response, messages = self.connection.search(None, criteria)
        
        email_ids = messages[0].split()
        
        # Get the last 'limit' number of emails
        if len(email_ids) > limit:
            email_ids = email_ids[-limit:]
        
        emails = []
        
        for email_id in email_ids:
            response, msg_data = self.connection.fetch(email_id, '(RFC822)')
            raw_email = msg_data[0][1]
            
            # Parse the raw email
            msg = email.message_from_bytes(raw_email)
            
            subject = self._decode_email_header(msg['Subject'])
            from_address = self._decode_email_header(msg['From'])
            date = msg['Date']
            
            # Get email body
            body = ""
            
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    
                    # Skip attachments
                    if "attachment" in content_disposition:
                        continue
                    
                    # Get text content
                    if content_type == "text/plain" or content_type == "text/html":
                        try:
                            body = part.get_payload(decode=True).decode('utf-8')
                        except:
                            try:
                                body = part.get_payload(decode=True).decode('latin-1')
                            except:
                                body = "Could not decode email body"
                        break
            else:
                # If email is not multipart
                try:
                    body = msg.get_payload(decode=True).decode('utf-8')
                except:
                    try:
                        body = msg.get_payload(decode=True).decode('latin-1')
                    except:
                        body = "Could not decode email body"
            
            email_data = {
                'id': email_id.decode(),
                'subject': subject,
                'from': from_address,
                'date': date,
                'body': body
            }
            
            emails.append(email_data)
        
        return emails
    
    def _decode_email_header(self, header):
        """
        Decode email headers
        """
        if header is None:
            return ""
            
        decoded_header = decode_header(header)
        header_parts = []
        
        for part, encoding in decoded_header:
            if isinstance(part, bytes):
                try:
                    if encoding:
                        header_parts.append(part.decode(encoding))
                    else:
                        header_parts.append(part.decode('utf-8'))
                except:
                    header_parts.append(part.decode('latin-1'))
            else:
                header_parts.append(part)
                
        return " ".join(header_parts) 