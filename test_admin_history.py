import requests
import json
import time

base_url = 'http://127.0.0.1:5000'

def test_admin_history():
    session = requests.Session()

    # Step 1: Login as admin
    login_data = {'username': 'alakh', 'password': 'alakh@123'}
    response = session.post(f'{base_url}/admin-login', data=login_data)
    if 'Invalid credentials' in response.text:
        print("Admin login failed")
        return False
    print("Admin login successful")

    # Step 2: Check /admin/history page has Reset History button
    response = session.get(f'{base_url}/admin/history')
    if 'Reset History' in response.text and 'View 10 Days History' in response.text:
        print("Reset History and View 10 Days History buttons are visible")
    else:
        print("Buttons not visible")
        return False

    # Step 3: Click Reset History (simulate by calling the route)
    response = session.get(f'{base_url}/admin/history/reset')
    # Check if redirected to /admin/history
    if response.url.endswith('/admin/history'):
        print("Reset History redirect successful")
    else:
        print("Reset History redirect failed")
        return False

    # Check history.json is empty
    with open('data/history.json', 'r') as f:
        history = json.load(f)
    if len(history) == 0:
        print("history.json is empty after reset")
    else:
        print("history.json is not empty after reset")
        return False

    # Check page shows no orders
    response = session.get(f'{base_url}/admin/history')
    if 'No orders' in response.text or len(history) == 0:
        print("Page shows no orders after reset")
    else:
        print("Page still shows orders after reset")
        return False

    # Step 4: Place 2 new orders
    user_session = requests.Session()
    user_session.post(f'{base_url}/guest')  # Login as guest

    order1 = {
        'cart': [{'name': 'Idli Sambar', 'price': 50}],
        'total': 50,
        'table': '1',
        'payment': 'Cash'
    }
    response = user_session.post(f'{base_url}/place_order', json=order1)
    if response.json().get('success'):
        print("Order 1 placed")
    else:
        print("Order 1 failed")
        return False

    order2 = {
        'cart': [{'name': 'Vada Pav', 'price': 20}],
        'total': 20,
        'table': '2',
        'payment': 'UPI'
    }
    response = user_session.post(f'{base_url}/place_order', json=order2)
    if response.json().get('success'):
        print("Order 2 placed")
    else:
        print("Order 2 failed")
        return False

    # Complete the orders to move to history
    with open('data/orders.json', 'r') as f:
        orders = json.load(f)
    order_ids = [o['id'] for o in orders]
    for oid in order_ids:
        session.post(f'{base_url}/admin/complete/{oid}')

    # Step 5: Click View 10 Days History
    response = session.get(f'{base_url}/admin/history/10days')
    if 'Idli Sambar' in response.text and 'Vada Pav' in response.text:
        print("View 10 Days History shows the 2 orders")
    else:
        print("View 10 Days History does not show the 2 orders")
        return False

    # Check revenue: Cash 50, UPI 20, Total 70
    if '₹50' in response.text and '₹20' in response.text and '₹70' in response.text:
        print("Revenue breakdown correct: Cash ₹50, UPI ₹20, Total ₹70")
        return True
    else:
        print("Revenue breakdown incorrect")
        return False

if __name__ == '__main__':
    time.sleep(2)  # Wait for app to start
    success = test_admin_history()
    if success:
        print("ALL TESTS PASSED!")
    else:
        print("TESTS FAILED")
