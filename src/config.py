"""
Configuration file for Hackathon 2025 Delivery Challenge
"""

# Server Configuration
SERVER_URL = "http://127.0.0.1:5000"
PASSWORD = "dummy_password"

# Competition Parameters
MAX_PACKAGES_PER_TRIP = 3
TOTAL_PACKAGES = 40  # Maximum packages in the competition

# Optimization Parameters
DISTANCE_WEIGHT = 0.1  # Weight for distance in profit calculation (adjusted for map scale)
REWARD_WEIGHT = 1.0    # Weight for reward in profit calculation

# Algorithm Selection
USE_ASTAR = True  # If False, use Dijkstra

# Logging
DEBUG = True
LOG_LEVEL = "INFO"

# Timeout and Retry
REQUEST_TIMEOUT = 10  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Polling interval for car state
POLL_INTERVAL = 0.5  # seconds
