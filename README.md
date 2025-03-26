# Function Execution API

## Overview
An intelligent API that uses semantic search to map user prompts to system automation functions.

## Features
- Semantic function discovery
- Session-based memory
- Comprehensive error logging
- System automation capabilities

## Setup
1. Clone the repository
2. Create virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run the API: `python main.py`

## Usage
Send POST requests to `/execute` with a prompt and optional parameters.

## Example
```bash
curl -X POST http://localhost:8000/execute \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Open Chrome", "params": {"url": "https://www.google.com"}}'