@echo off
echo Starting UrbanServe microservices...

start "User Service"    cmd /k "cd user_service    && python -m uvicorn main:app --port 8001 --reload"
start "Catalog Service" cmd /k "cd catalog_service && python -m uvicorn main:app --port 8002 --reload"
start "Booking Service" cmd /k "cd booking_service && python -m uvicorn main:app --port 8003 --reload"

timeout /t 3 >nul

start "API Gateway"     cmd /k "cd gateway         && python -m uvicorn main:app --port 8000 --reload"

echo All services started.
echo   Gateway:  http://localhost:8000
echo   Users:    http://localhost:8001
echo   Catalog:  http://localhost:8002
echo   Bookings: http://localhost:8003
