#!/usr/bin/env python3
"""
Simple test script to verify the backend API is working
"""

import requests
import json

def test_backend():
    base_url = "http://localhost:8000"
    
    print("Testing PCCE Backend API...")
    print("=" * 40)
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test 3: API documentation
    print("\n3. Testing API documentation...")
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("✅ API documentation accessible")
            print(f"   Visit: {base_url}/docs")
        else:
            print(f"❌ API documentation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API documentation error: {e}")
    
    # Test 4: Teams endpoint (should require auth)
    print("\n4. Testing teams endpoint (should require auth)...")
    try:
        response = requests.get(f"{base_url}/teams/")
        if response.status_code == 401:
            print("✅ Teams endpoint properly protected (requires authentication)")
        else:
            print(f"⚠️  Teams endpoint returned: {response.status_code}")
    except Exception as e:
        print(f"❌ Teams endpoint error: {e}")
    
    print("\n" + "=" * 40)
    print("Backend test completed!")
    print(f"API Documentation: {base_url}/docs")
    print(f"Health Check: {base_url}/health")
    
    return True

if __name__ == "__main__":
    test_backend()
