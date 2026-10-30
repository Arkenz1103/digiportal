"""
Test script for Portfolio Folder API
Run this to verify the API is working correctly
"""
import requests
import json

BASE_URL = 'http://localhost:8000'

def test_authentication():
    """Test authentication endpoint"""
    print("\n=== Testing Authentication ===")
    
    # Test GET (should fail initially)
    response = requests.get(f'{BASE_URL}/api/validate-session/')
    print(f"GET /api/validate-session/ - Status: {response.status_code}")
    
    # Test POST (create session)
    response = requests.post(
        f'{BASE_URL}/api/validate-session/',
        json={'role': 'teacher'}
    )
    print(f"POST /api/validate-session/ - Status: {response.status_code}")
    if response.status_code == 200:
        print(f"User: {response.json()['user']}")
    
    return response.cookies

def test_list_folders(cookies):
    """Test listing folders"""
    print("\n=== Testing List Folders ===")
    response = requests.get(
        f'{BASE_URL}/api/portfolio/folders/',
        cookies=cookies
    )
    print(f"GET /api/portfolio/folders/ - Status: {response.status_code}")
    if response.status_code == 200:
        folders = response.json()
        print(f"Found {len(folders)} folders")
        for folder in folders[:3]:  # Show first 3
            print(f"  - {folder['name']}: {folder.get('description', 'No description')}")
    return response

def test_create_folder(cookies):
    """Test creating a folder"""
    print("\n=== Testing Create Folder ===")
    
    folder_data = {
        'name': 'Test Portfolio',
        'description': 'This is a test portfolio folder created by the API test script'
    }
    
    response = requests.post(
        f'{BASE_URL}/api/portfolio/folders/',
        json=folder_data,
        cookies=cookies
    )
    
    print(f"POST /api/portfolio/folders/ - Status: {response.status_code}")
    
    if response.status_code == 201:
        folder = response.json()
        print(f"✓ Folder created successfully!")
        print(f"  ID: {folder['id']}")
        print(f"  Name: {folder['name']}")
        print(f"  Description: {folder['description']}")
        return folder['id']
    else:
        print(f"✗ Failed to create folder")
        print(f"  Error: {response.json()}")
        return None

def test_get_folder(folder_id, cookies):
    """Test getting a specific folder"""
    print(f"\n=== Testing Get Folder {folder_id} ===")
    response = requests.get(
        f'{BASE_URL}/api/portfolio/folders/{folder_id}/',
        cookies=cookies
    )
    print(f"GET /api/portfolio/folders/{folder_id}/ - Status: {response.status_code}")
    if response.status_code == 200:
        folder = response.json()
        print(f"  Name: {folder['name']}")
        print(f"  Description: {folder['description']}")

def test_update_folder(folder_id, cookies):
    """Test updating a folder"""
    print(f"\n=== Testing Update Folder {folder_id} ===")
    
    update_data = {
        'name': 'Updated Test Portfolio',
        'description': 'This description has been updated'
    }
    
    response = requests.put(
        f'{BASE_URL}/api/portfolio/folders/{folder_id}/',
        json=update_data,
        cookies=cookies
    )
    
    print(f"PUT /api/portfolio/folders/{folder_id}/ - Status: {response.status_code}")
    if response.status_code == 200:
        print(f"✓ Folder updated successfully!")

def test_delete_folder(folder_id, cookies):
    """Test deleting a folder"""
    print(f"\n=== Testing Delete Folder {folder_id} ===")
    
    response = requests.delete(
        f'{BASE_URL}/api/portfolio/folders/{folder_id}/',
        cookies=cookies
    )
    
    print(f"DELETE /api/portfolio/folders/{folder_id}/ - Status: {response.status_code}")
    if response.status_code == 204:
        print(f"✓ Folder deleted successfully!")

def main():
    """Run all tests"""
    print("=" * 50)
    print("Portfolio Folder API Test Suite")
    print("=" * 50)
    
    try:
        # Test authentication
        cookies = test_authentication()
        
        # Test listing folders
        test_list_folders(cookies)
        
        # Test creating a folder
        folder_id = test_create_folder(cookies)
        
        if folder_id:
            # Test getting the folder
            test_get_folder(folder_id, cookies)
            
            # Test updating the folder
            test_update_folder(folder_id, cookies)
            
            # Test deleting the folder
            test_delete_folder(folder_id, cookies)
        
        print("\n" + "=" * 50)
        print("✓ All tests completed!")
        print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to Django server")
        print("Make sure Django is running on http://localhost:8000")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")

if __name__ == '__main__':
    main()
