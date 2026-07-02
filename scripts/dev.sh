#!/bin/bash
set -euo pipefail

# Start backend in the background
echo "Starting backend server in development mode..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &

# Start frontend development server
echo "Starting frontend development server..."
cd frontend
npm run dev