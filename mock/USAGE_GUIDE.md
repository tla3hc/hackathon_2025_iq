# Mock Server Usage Guide

## Quick Start

### Windows
```bash
cd mock
start_server.bat
```

### Linux/Mac
```bash
cd mock
chmod +x start_server.sh
./start_server.sh
```

### Manual Start
```bash
cd mock
pip install flask
python mock_server.py
```

## Testing the Server

In a **separate terminal**, run the test suite:

```bash
cd mock
python test_mock_server.py
```

Expected output:
```
============================================================
MOCK SERVER TEST SUITE
============================================================
Testing server at: http://127.0.0.1:5000

[TEST 1] Health Check
----------------------------------------
Status: 200
Response: {
  "server_type": "HTTP",
  "status": "healthy",
  "timestamp": 1701619200.0
}
✓ PASSED

[TEST 2] Login
----------------------------------------
Wrong password status: 401
Correct password status: 200
Response: {'message': 'Login successful'}
Cookies received: ['session']
✓ PASSED

... (more tests)

============================================================
ALL TESTS PASSED! ✓
============================================================
```

## Running Your Solution Against Mock Server

### Terminal 1: Start Mock Server
```bash
cd mock
python mock_server.py
```

### Terminal 2: Run Your Solution
```bash
cd src
python main.py
```

You should see:
- **Mock Server Terminal**: Logs of API calls, route submissions, package deliveries
- **Solution Terminal**: Your algorithm selecting packages, optimizing routes, progress

## Example Session

### Mock Server Output:
```
============================================================
Mock Hackathon 2025 Server Starting...
============================================================
Server URL: http://127.0.0.1:5000
Password: dummy_password
============================================================

 * Running on http://127.0.0.1:5000

127.0.0.1 - - [03/Dec/2025 10:30:00] "POST /login HTTP/1.1" 200 -
127.0.0.1 - - [03/Dec/2025 10:30:00] "GET /road_information HTTP/1.1" 200 -
127.0.0.1 - - [03/Dec/2025 10:30:00] "GET /packages HTTP/1.1" 200 -
127.0.0.1 - - [03/Dec/2025 10:30:01] "GET /car HTTP/1.1" 200 -
127.0.0.1 - - [03/Dec/2025 10:30:01] "GET /get_tokens HTTP/1.1" 200 -
[Mock Server] Car starting route with index: 0
[Mock Server] Delivered packages: ['2', '5', '8']
127.0.0.1 - - [03/Dec/2025 10:30:01] "POST /set_index HTTP/1.1" 200 -
[Mock Server] Car stopped
```

### Your Solution Output:
```
============================================================
HACKATHON 2025 - DELIVERY OPTIMIZATION SYSTEM
============================================================

[1/4] Checking server health...
✓ Server healthy: healthy

[2/4] Authenticating...
✓ Login successful

[3/4] Loading road network...
✓ Graph built: 28 nodes, 86 edges

[4/4] Loading packages...
✓ Loaded 10 packages

✓ Initialization complete!
============================================================

============================================================
DELIVERY CYCLE #1
============================================================

📍 Current position: (178.25, 190.00)
📦 Undelivered packages: 10

🔑 Getting route tokens...
✓ Received 3 tokens

🎯 Selecting up to 3 packages...
✓ Selected 3 packages:
  - Package 2: (1127.00, 1350.00)
  - Package 5: (1321.00, 1589.00)
  - Package 8: (2018.00, 1270.00)

🚀 Optimizing delivery route...
✓ Route optimized:
  - Packages: 3
  - Distance: 2847.23
  - Reward: $3.00
  - Net Profit: $-2844.23

📤 Submitting route (index: 0)...
✓ Route index 0 submitted successfully

⏳ Waiting for car to stop...
✓ Delivery cycle complete!
  - Delivered: 3 packages
```

## API Testing with curl

### Health Check
```bash
curl http://127.0.0.1:5000/health
```

### Login and Save Cookies
```bash
curl -X POST http://127.0.0.1:5000/login \
  -d "password=dummy_password" \
  -c cookies.txt -v
```

### Get Road Information
```bash
curl http://127.0.0.1:5000/road_information -b cookies.txt
```

### Get Packages
```bash
curl http://127.0.0.1:5000/packages -b cookies.txt
```

### Get Car State
```bash
curl http://127.0.0.1:5000/car -b cookies.txt
```

### Get Tokens
```bash
curl http://127.0.0.1:5000/get_tokens -b cookies.txt
```

### Submit Route
```bash
curl -X POST http://127.0.0.1:5000/set_index \
  -H "Content-Type: application/json" \
  -d '{"index": 0}' \
  -b cookies.txt
```

### Reset Server State
```bash
curl http://127.0.0.1:5000/reset
```

## Troubleshooting

### Issue: Port Already in Use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solutions:**

1. Kill existing process:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

2. Change port in `mock_server.py`:
```python
app.run(host='127.0.0.1', port=8000, debug=True)
```

Then update `src/config.py`:
```python
SERVER_URL = "http://127.0.0.1:8000"
```

### Issue: Flask Not Installed

**Error:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
pip install flask
```

### Issue: Connection Refused

**Error:**
```
requests.exceptions.ConnectionError: Connection refused
```

**Solution:**
- Ensure mock server is running
- Check the URL in `src/config.py` matches the server
- Check firewall isn't blocking port 5000

### Issue: Authentication Failed

**Error:**
```
{"message": "Authentication required"}
```

**Solution:**
- Check cookies are being saved and sent
- Login again
- Use `/reset` endpoint to clear session

### Issue: No Packages Available

**Mock server shows all packages delivered**

**Solution:**
```bash
curl http://127.0.0.1:5000/reset
```

This resets the server state including packages.

## Customizing Mock Behavior

### Change Car Stop Time

Edit `mock_server.py`:
```python
def stop_car():
    time.sleep(random.uniform(5, 10))  # Change delay
    car_running = False
```

### Change Packages Delivered Per Route

Edit `mock_server.py`:
```python
num_to_deliver = min(2, len(available))  # Deliver 2 instead of 3
```

### Add Custom Logging

Edit `mock_server.py`:
```python
@app.before_request
def log_request():
    print(f"[{time.strftime('%H:%M:%S')}] {request.method} {request.path}")
```

### Change Password

Edit `mock_server.py`:
```python
PASSWORD = "your_custom_password"
```

Then update `src/config.py`:
```python
PASSWORD = "your_custom_password"
```

## Advanced Testing

### Stress Test
Run multiple clients simultaneously:

```bash
# Terminal 1: Mock server
python mock_server.py

# Terminal 2-4: Multiple clients
python ../src/main.py &
python ../src/main.py &
python ../src/main.py &
```

### Monitor Server Logs
```bash
python mock_server.py 2>&1 | tee server.log
```

### Test with Python Requests
```python
import requests

session = requests.Session()
session.post('http://127.0.0.1:5000/login', 
             data={'password': 'dummy_password'})

# All subsequent requests use same session
packages = session.get('http://127.0.0.1:5000/packages').json()
print(f"Packages: {len(packages)}")
```

## Integration Testing

Create a full test scenario:

```python
# test_scenario.py
from src.main import DeliveryController

def test_full_cycle():
    controller = DeliveryController()
    assert controller.initialize()
    
    # Run for 3 cycles
    for i in range(3):
        result = controller.execute_delivery_cycle()
        print(f"Cycle {i+1}: {result}")
    
    controller.print_summary()

if __name__ == "__main__":
    test_full_cycle()
```

## Performance Metrics

Track server performance:

```python
# In mock_server.py
import time

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_timing(response):
    if hasattr(request, 'start_time'):
        elapsed = time.time() - request.start_time
        print(f"[TIMING] {request.path}: {elapsed*1000:.2f}ms")
    return response
```

## Production vs Mock Differences

| Feature | Mock Server | Real Server |
|---------|-------------|-------------|
| Package rewards | All 1.0 | Variable |
| Dropoff locations | Static | Randomized |
| Car physics | Simplified timing | Real physics simulation |
| Token validation | Not validated | Validated |
| Obstacles | Static | Dynamic |
| Competition state | Single player | Multi-player |

## Mock Server Files

```
mock/
├── mock_server.py           # Main server implementation
├── requirements.txt         # Flask dependency
├── README.md               # Full documentation
├── USAGE_GUIDE.md          # This file
├── start_server.bat        # Windows start script
├── start_server.sh         # Linux/Mac start script
└── test_mock_server.py     # Test suite
```

## Next Steps

1. ✅ Start mock server
2. ✅ Run test suite
3. ✅ Run your solution
4. ✅ Monitor both terminals
5. ✅ Verify packages are delivered
6. ✅ Check statistics are correct
7. ✅ Test edge cases (all packages delivered, etc.)
8. ✅ Optimize algorithm based on results

---

**Happy Testing!** 🚀
