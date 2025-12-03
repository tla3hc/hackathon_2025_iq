"""
Test script to verify mock server is working correctly.
Run this while the mock server is running.
"""
import requests
import json
import time

SERVER_URL = "http://127.0.0.1:5000"
PASSWORD = "dummy_password"


def test_health():
    """Test health endpoint."""
    print("\n[TEST 1] Health Check")
    print("-" * 40)
    
    response = requests.get(f"{SERVER_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'
    print("✓ PASSED")


def test_login():
    """Test login."""
    print("\n[TEST 2] Login")
    print("-" * 40)
    
    # Test with wrong password
    response = requests.post(f"{SERVER_URL}/login", data={"password": "wrong"})
    print(f"Wrong password status: {response.status_code}")
    assert response.status_code == 401
    
    # Test with correct password
    response = requests.post(f"{SERVER_URL}/login", data={"password": PASSWORD})
    print(f"Correct password status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    cookies = response.cookies.get_dict()
    print(f"Cookies received: {list(cookies.keys())}")
    print("✓ PASSED")
    
    return cookies


def test_authenticated_endpoints(cookies):
    """Test endpoints that require authentication."""
    print("\n[TEST 3] Road Information")
    print("-" * 40)
    
    response = requests.get(f"{SERVER_URL}/road_information", cookies=cookies)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Points: {len(data.get('points', []))}")
    print(f"Streets: {len(data.get('streets', []))}")
    
    assert response.status_code == 200
    assert 'points' in data
    assert 'streets' in data
    print("✓ PASSED")
    
    print("\n[TEST 4] Packages")
    print("-" * 40)
    
    response = requests.get(f"{SERVER_URL}/packages", cookies=cookies)
    print(f"Status: {response.status_code}")
    packages = response.json()
    print(f"Available packages: {len(packages)}")
    print(f"Package IDs: {list(packages.keys())}")
    
    assert response.status_code == 200
    assert len(packages) > 0
    print("✓ PASSED")
    
    print("\n[TEST 5] Car State")
    print("-" * 40)
    
    response = requests.get(f"{SERVER_URL}/car", cookies=cookies)
    print(f"Status: {response.status_code}")
    car = response.json()
    print(f"Car state: {car.get('state')}")
    print(f"Position: {car.get('position')}")
    print(f"Orientation: {car.get('orientation')}")
    
    assert response.status_code == 200
    assert 'state' in car
    assert 'position' in car
    print("✓ PASSED")
    
    print("\n[TEST 6] Get Tokens")
    print("-" * 40)
    
    response = requests.get(f"{SERVER_URL}/get_tokens", cookies=cookies)
    print(f"Status: {response.status_code}")
    tokens_data = response.json()
    
    if 'tokens' in tokens_data:
        print(f"Tokens received: {len(tokens_data['tokens'])}")
        print("✓ PASSED")
    else:
        print(f"Message: {tokens_data.get('message')}")
        print("✓ PASSED (car may be running)")


def test_route_submission(cookies):
    """Test route submission."""
    print("\n[TEST 7] Route Submission")
    print("-" * 40)
    
    # Wait for car to be stopped
    print("Waiting for car to be in STOP state...")
    for _ in range(10):
        response = requests.get(f"{SERVER_URL}/car", cookies=cookies)
        car = response.json()
        if car.get('state') == 'STOP':
            print("Car is stopped")
            break
        time.sleep(0.5)
    
    # Submit route
    payload = {"index": 0}
    response = requests.post(
        f"{SERVER_URL}/set_index",
        json=payload,
        cookies=cookies
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    print("✓ PASSED")
    
    # Check car is now moving
    time.sleep(0.5)
    response = requests.get(f"{SERVER_URL}/car", cookies=cookies)
    car = response.json()
    print(f"Car state after submission: {car.get('state')}")
    
    # Wait for car to stop
    print("Waiting for car to complete route...")
    for i in range(15):
        response = requests.get(f"{SERVER_URL}/car", cookies=cookies)
        car = response.json()
        state = car.get('state')
        print(f"  [{i+1}] State: {state}")
        
        if state == 'STOP':
            print("Car stopped successfully")
            break
        time.sleep(0.5)
    
    print("✓ PASSED")


def test_reset():
    """Test reset endpoint."""
    print("\n[TEST 8] Reset Server")
    print("-" * 40)
    
    response = requests.get(f"{SERVER_URL}/reset")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    print("✓ PASSED")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("MOCK SERVER TEST SUITE")
    print("=" * 60)
    print(f"Testing server at: {SERVER_URL}")
    
    try:
        test_health()
        cookies = test_login()
        test_authenticated_endpoints(cookies)
        test_route_submission(cookies)
        test_reset()
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60)
        print("\nMock server is working correctly.")
        print("You can now run your solution with: python ../src/main.py")
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except requests.exceptions.ConnectionError:
        print("\n✗ CONNECTION ERROR")
        print("Make sure the mock server is running:")
        print("  python mock_server.py")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
