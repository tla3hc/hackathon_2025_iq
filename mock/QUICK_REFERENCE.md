# Mock Server - Quick Reference

## Start Server (Choose One)

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

### Manual
```bash
cd mock
python mock_server.py
```

## Test Server

```bash
cd mock
python test_mock_server.py
```

## Run Your Solution

Open **new terminal**:
```bash
cd src
python main.py
```

## Server Info

- **URL**: http://127.0.0.1:5000
- **Password**: dummy_password
- **Data**: Uses example_payload files

## Key Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/health` | GET | No | Health check |
| `/login` | POST | No | Login (password in body) |
| `/road_information` | GET | Yes | Get road network |
| `/packages` | GET | Yes | Get available packages |
| `/car` | GET | Yes | Get car state |
| `/get_tokens` | GET | Yes | Get route tokens |
| `/set_index` | POST | Yes | Submit route |
| `/reset` | GET | No | Reset server state |

## Quick curl Commands

```bash
# Login
curl -X POST http://127.0.0.1:5000/login -d "password=dummy_password" -c cookies.txt

# Get packages
curl http://127.0.0.1:5000/packages -b cookies.txt

# Get car state
curl http://127.0.0.1:5000/car -b cookies.txt

# Submit route
curl -X POST http://127.0.0.1:5000/set_index -H "Content-Type: application/json" -d '{"index": 0}' -b cookies.txt

# Reset
curl http://127.0.0.1:5000/reset
```

## Common Issues

| Problem | Solution |
|---------|----------|
| Port in use | Kill process or change port |
| Flask not found | `pip install flask` |
| Can't connect | Start mock server first |
| No packages | Use `/reset` endpoint |

## Files

- `mock_server.py` - Main server
- `test_mock_server.py` - Test suite
- `start_server.bat` - Windows launcher
- `start_server.sh` - Linux/Mac launcher
- `README.md` - Full docs
- `USAGE_GUIDE.md` - Detailed guide

## Typical Workflow

1. **Start mock server** (Terminal 1)
   ```bash
   cd mock
   python mock_server.py
   ```

2. **Test server** (Terminal 2)
   ```bash
   cd mock
   python test_mock_server.py
   ```

3. **Run solution** (Terminal 2)
   ```bash
   cd ../src
   python main.py
   ```

4. **Monitor both terminals**
   - Mock server: API calls, deliveries
   - Solution: Algorithm progress

5. **Reset if needed**
   ```bash
   curl http://127.0.0.1:5000/reset
   ```

---

📚 **Full docs**: See `README.md` and `USAGE_GUIDE.md`
