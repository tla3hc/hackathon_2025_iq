# Hackathon 2025 - Complete Project Structure

```
IQ/
│
├── requirement_and_rules/           # Competition rules and requirements
│   ├── requirement.md              # Official requirements (English)
│   ├── rules.txt                   # Competition rules
│   └── hackathon2025_IQ_overview_clean.txt
│
├── example_and_api/                # Reference materials from organizers
│   ├── controller_api_endpoints.md # API documentation
│   ├── example_client.py           # Reference implementation
│   ├── es256-cert.pem             # Certificate for JWT
│   ├── es256-public.key           # Public key for JWT
│   └── example_payload/            # Example API responses
│       ├── request_set_index.json
│       ├── response_car.json
│       ├── response_get_tokens.json
│       ├── response_health.json
│       ├── response_packages.json
│       └── response_road_information.json
│
├── src/                            # YOUR SOLUTION (Main code)
│   ├── main.py                     # ⭐ MAIN ENTRY POINT - Run this!
│   ├── api_client.py               # Server communication
│   ├── graph.py                    # A* & Dijkstra pathfinding
│   ├── package_selector.py         # Package selection strategies
│   ├── route_optimizer.py          # Route optimization
│   ├── advanced_strategies.py      # Additional algorithms
│   ├── config.py                   # Configuration (URL, password, weights)
│   ├── utils.py                    # Helper functions
│   ├── test_components.py          # Component testing
│   ├── simple_example.py           # Basic usage demo
│   ├── requirements.txt            # Python dependencies
│   ├── __init__.py                 # Package initialization
│   ├── README.md                   # Full documentation
│   ├── QUICKSTART.md              # Quick start guide
│   └── SOLUTION_OVERVIEW.md       # Strategy explanation
│
└── mock/                           # MOCK SERVER (For testing)
    ├── mock_server.py              # ⭐ Mock server - Run this for testing!
    ├── test_mock_server.py         # Test suite
    ├── start_server.bat            # Windows launcher
    ├── start_server.sh             # Linux/Mac launcher
    ├── requirements.txt            # Flask dependency
    ├── README.md                   # Mock server docs
    ├── USAGE_GUIDE.md             # Detailed usage guide
    ├── QUICK_REFERENCE.md         # Quick commands
    └── SUMMARY.md                 # Overview and quick start
```

## 🚀 Quick Start Commands

### For Testing (Local Development)

**Terminal 1: Start Mock Server**
```bash
cd mock
python mock_server.py
```

**Terminal 2: Run Your Solution**
```bash
cd src
python main.py
```

### For Competition (Real Server)

**Edit config first:**
```bash
# src/config.py
SERVER_URL = "http://competition-server-url:port"
PASSWORD = "competition_password"
```

**Then run:**
```bash
cd src
python main.py
```

## 📊 File Categories

### 🎯 Core Solution Files (src/)
- `main.py` - Main controller, orchestrates everything
- `api_client.py` - All API communication
- `graph.py` - Pathfinding algorithms
- `package_selector.py` - Package selection logic
- `route_optimizer.py` - Route optimization
- `config.py` - All configuration

### 🧪 Testing & Examples (src/)
- `test_components.py` - Unit tests
- `simple_example.py` - Basic demo
- `advanced_strategies.py` - Advanced algorithms

### 📚 Documentation (src/)
- `README.md` - Complete documentation
- `QUICKSTART.md` - Step-by-step guide
- `SOLUTION_OVERVIEW.md` - Strategy explanation

### 🔧 Mock Server (mock/)
- `mock_server.py` - Flask server
- `test_mock_server.py` - Server tests
- `start_server.bat/sh` - Quick launchers

### 📖 Reference (example_and_api/)
- API documentation
- Example payloads
- Reference client code

### 📋 Requirements (requirement_and_rules/)
- Competition rules
- Problem statement
- Requirements

## 🎯 Most Important Files

### To Run Competition:
1. **`src/main.py`** - Your main program
2. **`src/config.py`** - Configure server and parameters

### To Test Locally:
1. **`mock/mock_server.py`** - Start mock server
2. **`src/main.py`** - Run solution against mock

### To Understand System:
1. **`src/README.md`** - Complete documentation
2. **`src/SOLUTION_OVERVIEW.md`** - Strategy explained
3. **`mock/SUMMARY.md`** - Mock server overview

## 📈 Development Workflow

```
1. Read Requirements
   └─> requirement_and_rules/requirement.md

2. Understand APIs
   └─> example_and_api/controller_api_endpoints.md
   └─> example_and_api/example_payload/

3. Test Locally
   └─> Start: mock/mock_server.py
   └─> Run: src/main.py

4. Optimize Algorithm
   └─> Edit: src/package_selector.py
   └─> Edit: src/route_optimizer.py
   └─> Edit: src/config.py (tune weights)

5. Compete
   └─> Update: src/config.py (real server URL)
   └─> Run: src/main.py
```

## 💡 Key Features by File

### main.py
- Initialization (login, load data)
- Delivery cycle loop
- Progress monitoring
- Statistics tracking

### api_client.py
- All 8 API endpoints
- Authentication
- Cookie management
- Error handling

### graph.py
- A* algorithm
- Dijkstra algorithm
- Graph building
- Path finding

### package_selector.py
- Greedy selection
- Density-based selection
- Profit calculation
- Multiple strategies

### route_optimizer.py
- Nearest neighbor
- Brute force optimization
- Distance calculation
- Route evaluation

### config.py
- Server URL and password
- Algorithm parameters
- Weights for profit calculation
- Tunable constants

### mock_server.py
- Complete API simulation
- Car state management
- Package delivery tracking
- Uses example payloads

## 🔍 Finding What You Need

**Want to change selection strategy?**
→ `src/package_selector.py`

**Want to adjust profit calculation?**
→ `src/config.py` (DISTANCE_WEIGHT, REWARD_WEIGHT)

**Want to test locally?**
→ Start `mock/mock_server.py`, run `src/main.py`

**Need to understand algorithm?**
→ `src/SOLUTION_OVERVIEW.md`

**Quick start guide?**
→ `src/QUICKSTART.md` or `mock/QUICK_REFERENCE.md`

**API reference?**
→ `example_and_api/controller_api_endpoints.md`

**Competition rules?**
→ `requirement_and_rules/requirement.md`

## 📦 Dependencies

### Solution (src/)
```bash
pip install requests pyjwt
```

### Mock Server (mock/)
```bash
pip install flask
```

## 🎓 Learning Path

1. **Start here**: `requirement_and_rules/requirement.md`
2. **Understand APIs**: `example_and_api/controller_api_endpoints.md`
3. **Quick start**: `src/QUICKSTART.md`
4. **Run example**: `src/simple_example.py`
5. **Test locally**: Start `mock/mock_server.py`
6. **Run solution**: `src/main.py`
7. **Optimize**: Adjust `src/config.py` weights
8. **Advanced**: `src/advanced_strategies.py`

## 🏆 Competition Day Checklist

- [ ] Read `requirement_and_rules/requirement.md`
- [ ] Test with `mock/mock_server.py`
- [ ] Run `src/test_components.py` (all pass)
- [ ] Update `src/config.py` with real server URL
- [ ] Verify login credentials
- [ ] Backup your `src/` folder
- [ ] Ready to compete!

---

**Everything you need to win is here!** 🚀
