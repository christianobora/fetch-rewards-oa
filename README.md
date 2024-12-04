# Points Management API

A FastAPI-based application for managing user points, including adding, spending, and retrieving balances.

## Features
- Add points for a payer.
- Spend points in FIFO order while respecting payer constraints.
- Fetch current balances per payer.

## Endpoints
1. `POST /add`: Add points for a payer.
   - **Request**:
     ```json
     {
       "payer": "DANNON",
       "points": 1000,
       "timestamp": "2022-10-31T10:00:00Z"
     }
     ```
   - **Response**:
     ```json
     {
       "message": "Points added successfully"
     }
     ```

2. `POST /spend`: Spend points.
   - **Request**:
     ```json
     {
       "points": 1500
     }
     ```
   - **Response**:
     ```json
     [
       { "payer": "DANNON", "points": -1000 },
       { "payer": "MILLER COORS", "points": -500 }
     ]
     ```

3. `GET /balance`: Fetch the current balances per payer.
   - **Response**:
     ```json
     {
       "balances": {
         "DANNON": 500,
         "MILLER COORS": 5300
       }
     }
     ```

## Running the Project
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
    uvicorn app.main:app --reload
   ```
3. Access the API documentation at `http://localhost:8000/docs`.