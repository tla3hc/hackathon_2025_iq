"""
API Client for Hackathon 2025 Delivery Challenge
Handles all communication with the competition server.
"""
import requests
import json
import jwt
import time
from typing import Dict, List, Tuple, Optional
from config import SERVER_URL, PASSWORD, REQUEST_TIMEOUT, MAX_RETRIES, RETRY_DELAY


class APIClient:
    """Client for interacting with the competition server API."""
    
    def __init__(self, server_url: str = SERVER_URL, password: str = PASSWORD):
        """
        Initialize API client.
        
        Args:
            server_url: Base URL of the competition server
            password: Authentication password
        """
        self.server_url = server_url
        self.password = password
        self.session = requests.Session()  # Use Session to persist cookies
        self.authenticated = False
    
    def login(self) -> bool:
        """
        Authenticate with the server.
        
        Returns:
            True if login successful, False otherwise
        """
        try:
            response = self.session.post(
                f'{self.server_url}/login',
                data={"password": self.password},
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                self.authenticated = True
                print("✓ Login successful")
                return True
            else:
                print(f"✗ Login failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Login error: {e}")
            return False
    
    def logout(self) -> bool:
        """Logout from the server."""
        try:
            response = self.session.get(
                f'{self.server_url}/logout',
                timeout=REQUEST_TIMEOUT
            )
            self.authenticated = False
            self.session.cookies.clear()
            print("✓ Logged out")
            return True
        except Exception as e:
            print(f"✗ Logout error: {e}")
            return False
    
    def check_health(self) -> Optional[Dict]:
        """
        Check server health.
        
        Returns:
            Health status dict or None if failed
        """
        try:
            response = self.session.get(
                f'{self.server_url}/health',
                timeout=REQUEST_TIMEOUT
            )
            if response.status_code == 200:
                return json.loads(response.text)
            return None
        except Exception as e:
            print(f"✗ Health check error: {e}")
            return None
    
    def get_road_information(self) -> Optional[Dict]:
        """
        Get road network information.
        
        Returns:
            Dict with 'points' and 'streets' or None if failed
        """
        if not self.authenticated:
            print("✗ Not authenticated. Please login first.")
            return None
        
        try:
            response = self.session.get(
                f'{self.server_url}/road_information',
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                print(f"✗ Failed to get road info: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"✗ Road information error: {e}")
            return None
    
    def get_packages(self) -> Optional[Dict]:
        """
        Get available packages.
        
        Returns:
            Dict of packages {id: {id, position}} or None if failed
        """
        if not self.authenticated:
            print("✗ Not authenticated. Please login first.")
            return None
        
        try:
            response = self.session.get(
                f'{self.server_url}/packages',
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                print(f"✗ Failed to get packages: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"✗ Packages error: {e}")
            return None
    
    def get_car_state(self) -> Optional[Dict]:
        """
        Get current car state.
        
        Returns:
            Dict with 'state', 'position', 'orientation', 'obstacles' or None
        """
        if not self.authenticated:
            print("✗ Not authenticated. Please login first.")
            return None
        
        try:
            response = self.session.get(
                f'{self.server_url}/car',
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                print(f"✗ Failed to get car state: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"✗ Car state error: {e}")
            return None
    
    def get_tokens(self) -> Optional[Dict]:
        """
        Get tokens for verification.
        
        Returns:
            Dict with 'tokens' list or message, or None if failed
        """
        if not self.authenticated:
            print("✗ Not authenticated. Please login first.")
            return None
        
        try:
            response = self.session.get(
                f'{self.server_url}/get_tokens',
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                print(f"✗ Failed to get tokens: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"✗ Tokens error: {e}")
            return None
    
    def set_route_index(self, index: int) -> bool:
        """
        Submit route index to the server.
        
        Args:
            index: Route index to follow
        
        Returns:
            True if successful, False otherwise
        """
        if not self.authenticated:
            print("✗ Not authenticated. Please login first.")
            return False
        
        try:
            payload = {"index": index}
            response = self.session.post(
                f'{self.server_url}/set_index',
                json=payload,
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                print(f"✓ Route index {index} submitted successfully")
                return True
            else:
                print(f"✗ Failed to set route index: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Set route index error: {e}")
            return False
    
    def wait_for_car_stop(self, poll_interval: float = 0.5, timeout: float = 300) -> bool:
        """
        Wait for car to reach STOP state.
        
        Args:
            poll_interval: Time between state checks in seconds
            timeout: Maximum wait time in seconds
        
        Returns:
            True if car stopped, False if timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            car_state = self.get_car_state()
            
            if car_state and car_state.get('state') == 'STOP':
                return True
            
            time.sleep(poll_interval)
        
        print(f"✗ Timeout waiting for car to stop")
        return False
    
    def decode_token(self, token: str) -> Optional[Dict]:
        """
        Decode JWT token without verification.
        
        Args:
            token: JWT token string
        
        Returns:
            Decoded payload or None if failed
        """
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload
        except Exception as e:
            print(f"✗ Token decode error: {e}")
            return None
