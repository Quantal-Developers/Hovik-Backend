# Backend API - Batch Lookup Service

## Description

A FastAPI-based REST API service that retrieves batch information and associated Google Drive document links from a Google Sheets database. The API allows clients to query batch numbers and receive corresponding PDF document links stored in Google Drive.

## Overview

The backend service:
- Connects to Google Sheets using Google Service Account credentials
- Searches for batch numbers in the spreadsheet
- Returns batch information along with associated Google Drive document links (LINK1, LINK2, etc.)
- Provides CORS support for frontend integration
- Includes automatic API documentation via FastAPI/Swagger UI

## Prerequisites

- Python 3.8 or higher
- Google Service Account credentials file (`credentials.json`)
- Access to a Google Sheet with batch data
- Environment variables configured (optional)

## Installation

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up Google Service Account:**
   - Place your `credentials.json` file in the `backend` directory
   - Ensure the service account has access to your Google Sheet

6. **Configure environment variables (optional):**
   Create a `.env` file in the `backend` directory:
   ```env
   SHEET_NAME=BATCH_details
   WORKSHEET_NAME=Sheet1
   ```

## Running the Server

**Start the development server:**
```bash
uvicorn main:app --reload
```

The API will be available at:
- **API Base URL:** `http://localhost:8000`
- **API Documentation:** `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs:** `http://localhost:8000/redoc` (ReDoc)

## API Endpoints

### GET `/api/batch`

Retrieves batch information and document links by lot number.

**Query Parameters:**
- `lot_number` (required): The batch/lot number to search for

**Response Format:**
```json
{
  "BATCH": "BATCH01",
  "LINK1": "https://drive.google.com/file/d/.../view?usp=sharing",
  "LINK2": "https://drive.google.com/file/d/.../view?usp=sharing"
}
```

**Error Response (404):**
```json
{
  "error": "Lot number not found"
}
```

## Testing with Dummy Values

### Using Swagger UI (Recommended)

1. Open your browser and navigate to: `http://localhost:8000/docs`
2. Find the `GET /api/batch` endpoint
3. Click "Try it out"
4. Enter `lot_number` as `BATCH01`
5. Click "Execute"
6. You should see a response with BATCH, LINK1, and LINK2 fields

### Using cURL

```bash
curl -X 'GET' 'http://localhost:8000/api/batch?lot_number=BATCH01' -H 'accept: application/json'
```

### Using Browser

Simply open:
```
http://localhost:8000/api/batch?lot_number=BATCH01
```

### Expected Response for BATCH01

```json
{
  "BATCH": "BATCH01",
  "LINK1": "https://drive.google.com/file/d/1cAwbb7cb101M9cLg9I0nvyPYm2A81pIY/view?usp=sharing",
  "LINK2": "https://drive.google.com/file/d/1yp4oEUqM2pwJFB5brk-1cKfeUMWV4HNJ/view?usp=sharing"
}
```

## How It Works

1. **Request Flow:**
   - Client sends GET request with `lot_number` query parameter
   - Router receives request and calls the batch service
   - Service queries Google Sheets for matching batch number
   - Returns batch data with associated document links

2. **Google Sheets Integration:**
   - Uses `gspread` library to connect to Google Sheets
   - Authenticates using service account credentials
   - Searches for batch number in the first column
   - Returns data from matching row (BATCH, LINK1, LINK2)

3. **CORS Configuration:**
   - Configured to allow requests from frontend development servers
   - Supports common ports: 3000, 5173, 5174

## Project Structure

```
backend/
├── main.py                 # FastAPI application and CORS configuration
├── requirements.txt        # Python dependencies
├── credentials.json        # Google Service Account credentials (not in repo)
├── .env                    # Environment variables (optional)
├── routers/
│   └── batch_router.py     # API route definitions
└── services/
    └── batch_service.py    # Business logic and Google Sheets integration
```

## Troubleshooting

**Issue: "Failed to connect to Google Sheets"**
- Verify `credentials.json` is in the backend directory
- Check that the service account has access to the Google Sheet
- Ensure the sheet name matches your configuration

**Issue: "CORS error in frontend"**
- Verify the frontend URL is in the `allow_origins` list in `main.py`
- Restart the backend server after making changes

**Issue: "Module not found"**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

## Development

To run with auto-reload (development mode):
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

