#!/bin/bash

# Calculate the number of workers based on the system's CPU cores
workers=$(python -c "import os; print(max(1, min(os.cpu_count(), 9)))")

# Start the first application with the calculated number of workers
exec uvicorn app:app --host 0.0.0.0 --port 5000 --workers $workers
