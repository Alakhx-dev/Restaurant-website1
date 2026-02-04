import requests
import json
import time

base_url = 'http://127.0.0.1:5000'

def test_flow():
    session = requests.Session()

    # Step 1: Login as admin
    login_data = {'username': 'alakh', 'password': 'alakh@123'}
    response = session.post(f'{base_url}/admin-login', data=login_data)
    if 'Invalid credentials' in response.text:
        print("Admin login failed")
        return False
    print("Admin login successful")

    # Step 2: Check initial orders (should be empty)
    response = session.get(f'{base_url}/admin')
    if 'No orders' in response.text or 'orders' not in response.text.lower():
        print("Initial orders: empty (good)")
    else:
        print("Initial orders: not empty")
        return False

    # Step 3: Place 2 orders (simulate via /place_order)
    # First, need to login as user or use guest
    user_session = requests.Session()
    user_session.post(f'{base_url}/guest')  # Login as guest

    order1 = {
        'cart': [{'name': 'Idli Sambar', 'price': 50}],
        'total': 50,
        'table': '1',
        'payment': 'cash'
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
        'payment': 'upi'
    }
    response = user_session.post(f'{base_url}/place_order', json=order2)
    if response.json().get('success'):
        print("Order 2 placed")
    else:
        print("Order 2 failed")
        return False

    # Step 4: Check admin dashboard (should have 2 orders)
    response = session.get(f'{base_url}/admin')
    if 'Idli Sambar' in response.text and 'Vada Pav' in response.text:
        print("Admin dashboard shows 2 orders")
    else:
        print("Admin dashboard does not show 2 orders")
        return False

    # Step 5: Complete both orders
    # Extract order IDs from dashboard (simplified, assume we can parse)
    # For simplicity, since we can't easily parse HTML, check orders.json directly
    # But to follow the flow, assume we complete them via API if possible
    # The complete route is /admin/complete/<order_id>, but we need order IDs
    # For now, check orders.json after placing
    with open('data/orders.json', 'r') as f:
        orders = json.load(f)
    if len(orders) == 2:
        print("Orders.json has 2 orders")
        order_ids = [o['id'] for o in orders]
    else:
        print("Orders.json does not have 2 orders")
        return False

    # Complete first order
    response = session.post(f'{base_url}/admin/complete/{order_ids[0]}')
    print("Completed order 1")

    # Complete second order
    response = session.post(f'{base_url}/admin/complete/{order_ids[1]}')
    print("Completed order 2")

    # Step 6: Check orders.json is empty
    with open('data/orders.json', 'r') as f:
        orders = json.load(f)
    if len(orders) == 0:
        print("Orders.json is empty after completion")
    else:
        print("Orders.json is not empty after completion")
        return False

    # Step 7: Place 1 new order
    order3 = {
        'cart': [{'name': 'Poha', 'price': 40}],
        'total': 40,
        'table': '3',
        'payment': 'cash'
    }
    response = user_session.post(f'{base_url}/place_order', json=order3)
    if response.json().get('success'):
        print("New order placed")
    else:
        print("New order failed")
        return False

    # Step 8: Check admin dashboard shows ONLY the new order
    response = session.get(f'{base_url}/admin')
    if 'Poha' in response.text and 'Idli Sambar' not in response.text and 'Vada Pav' not in response.text:
        print("Admin dashboard shows ONLY the new order")
        return True
    else:
        print("Admin dashboard shows old orders or not the new one")
        return False

if __name__ == '__main__':
    time.sleep(2)  # Wait for app to start
    success = test_flow()
    if success:
        print("TEST PASSED: Bug fixed!")
    else:
        print("TEST FAILED: Bug still present")
