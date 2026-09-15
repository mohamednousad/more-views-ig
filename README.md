# FastAPI University Assignment

This project is structured as a scalable FastAPI application, designed to demonstrate the transition from traditional synchronous frameworks to asynchronous capabilities. It is suitable for high-performance tasks such as AI-driven vehicle valuation endpoints or automated web traffic simulations. 

The architecture is modular, making it straightforward to integrate a NoSQL database like MongoDB for persistent data storage later in the coursework.

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Access the interactive API docs at `http://127.0.0.1:8000/docs` to test the endpoints.
