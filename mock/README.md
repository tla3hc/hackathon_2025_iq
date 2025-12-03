# Mock Server for Testing

## Overview
This mock server simulates the competition server for local testing. It uses the example payloads from the `example_and_api/example_payload` folder.

## Features
- ✅ All API endpoints implemented
- ✅ Session-based authentication
- ✅ Simulated car movement and states
- ✅ Package delivery tracking
- ✅ Token generation
- ✅ Realistic timing simulation

## Installation

```bash
pip install -r requirements.txt
```

Or install Flask directly:
```bash
pip install flask
```

## Running the Mock Server

### Start the server:
```bash
python mock_server.py
```

The server will start on `http://127.0.0.1:5000`

### In a separate terminal, run your solution:
```bash
cd ../src
python main.py
```

## API Endpoints

All endpoints match the real competition server:

- `GET /` - Homepage with endpoint listing
- `GET /health` - Health check
- `POST /login` - Login (password: `dummy_password`)
- `GET /logout` - Logout
- `GET /road_information` - Get road network (requires auth)
- `GET /packages` - Get available packages (requires auth)
- `GET /car` - Get car state (requires auth)
- `GET /get_tokens` - Get route tokens (requires auth)
- `POST /set_index` - Submit route index (requires auth)
- `GET /reset` - Reset server state (testing only)

## Server Behavior

### Authentication
- Password: `dummy_password`
- Uses session cookies for authentication
- Returns 401 if not authenticated

### Car Simulation
- **STOP state**: When no route is active
- **Moving states**: MOVE_FORWARD, TURN, BLOCKED (randomized)
- **Auto-stop**: Car automatically stops after 2-5 seconds
- **Position changes**: Simulated with small random offsets

### Package Delivery
- Starts with 10 packages (from example payload)
- Delivers 1-3 random packages per route submission
- Tracks delivered packages
- `/packages` endpoint filters out delivered packages

### Tokens
- Returns JWT tokens from example payload
- Available only when car is in STOP state
- Token coordinates: [200.0, 187.0]

## Testing Workflow

1. **Start mock server:**
```bash
cd mock
python mock_server.py
```

2. **In another terminal, test your solution:**
```bash
cd ../src
python main.py
```

3. **Watch the logs:**
- Mock server shows: login, route submissions, package deliveries
- Your client shows: selected packages, routes, progress

4. **Reset if needed:**
```bash
curl http://127.0.0.1:5000/reset
```

## Server Output Example

```
============================================================
Mock Hackathon 2025 Server Starting...
============================================================
Server URL: http://127.0.0.1:5000
Password: dummy_password
============================================================

Available endpoints:
  GET  /health
  POST /login
  GET  /logout
  GET  /road_information
  GET  /packages
  GET  /car
  GET  /get_tokens
  POST /set_index
  GET  /reset (testing only)
============================================================

Press Ctrl+C to stop the server

 * Running on http://127.0.0.1:5000

[Mock Server] Car starting route with index: 0
[Mock Server] Delivered packages: ['3', '7', '9']
[Mock Server] Car stopped
```

## Manual Testing with curl

### Health check:
```bash
curl http://127.0.0.1:5000/health
```

### Login:
```bash
curl -X POST http://127.0.0.1:5000/login \
  -d "password=dummy_password" \
  -c cookies.txt
```

### Get packages:
```bash
curl http://127.0.0.1:5000/packages -b cookies.txt
```

### Get car state:
```bash
curl http://127.0.0.1:5000/car -b cookies.txt
```

### Submit route:
```bash
curl -X POST http://127.0.0.1:5000/set_index \
  -H "Content-Type: application/json" \
  -d '{"index": 0}' \
  -b cookies.txt
```

### Reset server:
```bash
curl http://127.0.0.1:5000/reset
```

## Configuration

Edit `mock_server.py` to customize:

```python
# Authentication
PASSWORD = "dummy_password"

# Car behavior
time.sleep(random.uniform(2, 5))  # Stop delay

# Package delivery
num_to_deliver = min(3, len(available))  # Packages per route
```

## Differences from Real Server

The mock server has some simplifications:

1. **Package rewards**: All set to 1.0 (not in example payload)
2. **Dropoff locations**: Not randomized (would need additional logic)
3. **Route execution**: Simplified timing (real server has physics)
4. **Token validation**: Not validated (mock accepts any index)
5. **Obstacles**: Static (real server has dynamic obstacles)

## Troubleshooting

**Port already in use:**
```
OSError: [Errno 48] Address already in use
```
Solution: Kill existing process or change port in `mock_server.py`

**Flask not found:**
```
ModuleNotFoundError: No module named 'flask'
```
Solution: `pip install flask`

**Session issues:**
Solution: Use `/reset` endpoint or restart server

**Import errors:**
Solution: Ensure you're running from the `mock` directory

## Advanced Usage

### Running on different port:
```python
app.run(host='127.0.0.1', port=8000, debug=True)
```

### Adding custom behavior:
```python
@app.route('/custom_endpoint')
def custom():
    return jsonify({"custom": "data"})
```

### Logging requests:
```python
@app.before_request
def log_request():
    print(f"[{request.method}] {request.path}")
```

## Integration with Your Solution

No changes needed! Just ensure `config.py` points to the mock server:

```python
# src/config.py
SERVER_URL = "http://127.0.0.1:5000"
PASSWORD = "dummy_password"
```

Then run normally:
```bash
python main.py
```

---

**Happy Testing!** 🚀
