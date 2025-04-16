# Email Parser Application

A Python application for parsing and processing emails.

## Features

- Connect to email servers via IMAP
- Parse email content (HTML and plain text)
- Extract data from structured emails
- Export parsed data to CSV/Excel
- Simple web interface for configuration and monitoring

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your email credentials:
   ```
   EMAIL_USER=your_email@example.com
   EMAIL_PASSWORD=your_password
   EMAIL_SERVER=imap.example.com
   EMAIL_PORT=993
   ```

## Usage

Run the application:

```
python app/app.py
```

Then open your browser and navigate to `http://localhost:5000`.

## Project Structure

- `app/app.py`: Main application entry point
- `app/utils/`: Utility functions for email parsing
- `app/models/`: Data models
- `app/controllers/`: Business logic
- `app/templates/`: HTML templates for web interface 