#!/bin/bash

echo "Starting PCCE Project Development Servers..."

echo ""
echo "Starting Backend Server..."
cd backend
python main.py &
BACKEND_PID=$!

echo ""
echo "Waiting 5 seconds for backend to start..."
sleep 5

echo ""
echo "Starting Frontend Server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "Both servers are starting..."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers..."

# Function to cleanup processes
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT

# Wait for processes
wait
