from flask import Flask, render_template, request, session, redirect, url_for, jsonify, send_file
import random
import string
from datetime import datetime, timedelta
import json
import os
import uuid
import io
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production

ORDERS_FILE = 'data/orders.json'
HISTORY_FILE = 'data/history.json'

# Menu data: Strictly vegetarian, categorized
menu = {
    'BREAKFAST': [
        {'name': 'Poha', 'price': 40, 'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSLqPQSDkyw94CAAnixNk_7gUINCmX2SScbhg&s'},
        {'name': 'Idli Sambar', 'price': 50, 'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJnB2lNVTmdNvzMLHiHkcbvGlrffbOlbnidg&s'},
        {'name': 'Vada Pav', 'price': 20, 'image': 'data:image/jpeg;base64,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'},
        {'name': 'Upma', 'price': 35, 'image': 'https://www.kuchpakrahahai.in/wp-content/uploads/2016/09/Vegetable-rawa-upma.jpg'}
    ],
    'LUNCH': [
        {'name': 'Veg Thali', 'price': 120, 'image': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?q=80&w=1000&auto=format&fit=crop'},
        {'name': 'Paneer Butter Masala', 'price': 150, 'image': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?q=80&w=1000&auto=format&fit=crop'},
        {'name': 'Dal Tadka', 'price': 80, 'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQzr1eTxZ2MWmggnntB6p6RvvXZq42Kp-dRDg&s'},
        {'name': 'Jeera Rice', 'price': 70, 'image': 'https://lentillovingfamily.com/wp-content/uploads/2025/08/jeera-rice-1-500x500.jpg'},
        {'name': 'Mix Veg Curry', 'price': 110, 'image': 'https://www.indianhealthyrecipes.com/wp-content/uploads/2023/07/vegetable-curry-recipe.jpg'},
        {'name': 'Soya Chaap', 'price': 130, 'image': 'https://i0.wp.com/upbeetanisha.com/wp-content/uploads/2024/01/IMG_9751.jpg?w=1200&ssl=1'}
    ],
    'DINNER': [
        {'name': 'Veg Biryani', 'price': 130, 'image': 'https://images.unsplash.com/photo-1589302168068-964664d93dc0?q=80&w=1000&auto=format&fit=crop'},
        {'name': 'Aloo Paratha ', 'price': 20, 'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSNxGEDa0EGCFKGFTAsWhshfZGYKezVAytndw&s'},
        {'name': 'Rajma Chawal', 'price': 100, 'image': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?q=80&w=1000&auto=format&fit=crop'},
        {'name': 'Mushroom Curry', 'price': 180, 'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTSVnbhIcraWm1sJepm2p59PooXjDtl8VdezA&s'},
         {'name': 'Pulao Rice', 'price': 180, 'image': 'https://www.flavourstreat.com/wp-content/uploads/2022/05/vegan-pulao-recipe.jpg'}
    ],
    'BEVERAGES': [
        {'name': 'Masala Chai', 'price': 20, 'image': 'https://cdn.shopify.com/s/files/1/0758/6929/0779/files/Masala_Tea_-_Annams_Recipes_Shop_2_480x480.jpg?v=1732347934'},
        {'name': 'Mango Lassi', 'price': 40, 'image': 'https://images.unsplash.com/photo-1571115177098-24ec42ed204d?q=80&w=1000&auto=format&fit=crop'}
    ]
}

# Helper functions for JSON storage
def load_json(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return []

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# Load data
completed_orders = load_json('data/history.json')

def normalize_order(order):
    order["date_time"] = order.get("date_time") or order.get("timestamp") or ""
    order["payment_method"] = (
        order.get("payment_method")
        or order.get("payment")
        or order.get("method")
        or "Cash"
    ).lower()
    return {
        'id': order.get('id') or order.get('order_id'),
        'table': order.get('table') or order.get('table_no'),
        'order_items': order.get('order_items') or order.get('items') or [],
        'total': order.get('total', 0),
        'user': order.get('user'),
        'payment_method': order["payment_method"],
        'date_time': order["date_time"]
    }

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('menu_page'))
    return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    return render_template('auth.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    # Simple in-memory user storage (use database in production)
    if 'users' not in app.config:
        app.config['users'] = {}
    if username in app.config['users']:
        return 'User already exists', 400
    app.config['users'][username] = password
    session['user'] = username
    return redirect(url_for('menu_page'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if app.config.get('users', {}).get(username) == password:
        session['user'] = username
        return redirect(url_for('menu_page'))
    return 'Invalid credentials', 400

@app.route('/guest')
def guest():
    # Support GET redirect and POST JSON to create a guest with a name
    if request.method == 'POST' or request.is_json:
        try:
            data = request.get_json(force=True)
        except Exception:
            data = None
        name = None
        if data and 'name' in data and data['name'].strip():
            name = data['name'].strip()
        else:
            # fallback guest id
            name = 'Guest_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        session['user'] = name
        return jsonify({'status': 'ok', 'user': name, 'redirect': url_for('menu_page')})
    # default GET behaviour: simple guest
    session['user'] = 'Guest'
    return redirect(url_for('menu_page'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login_page'))

@app.route('/menu')
def menu_page():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    return render_template('index.html', menu=menu, user=session['user'])

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item = request.json
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(item)
    session.modified = True
    return jsonify({'status': 'added'})

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    item_name = request.json['name']
    if 'cart' in session:
        # remove only one instance of the item (decrement quantity)
        for idx, it in enumerate(session['cart']):
            if it.get('name') == item_name:
                session['cart'].pop(idx)
                break
        session.modified = True
    return jsonify({'status': 'removed'})

@app.route('/get_cart')
def get_cart():
    return jsonify(session.get('cart', []))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            cart = data['cart']
            total = data['total']
            table_no = data['table_no']
            payment = data['payment']
            language = data.get('language')
        else:
            table_no = request.form['table_no']
            payment = request.form['payment']
            language = request.form.get('language')
            cart_data = request.form.get('cart_data')
            total_data = request.form.get('total_data')
            if cart_data and total_data:
                cart = json.loads(cart_data)
                total = float(total_data)
            else:
                cart = session.get('cart', [])
                total = sum(item['price'] for item in cart)
        order_id = str(uuid.uuid4())[:8]
        order = {
            'id': order_id,
            'table': table_no,
            'order_items': cart,
            'total': total,
            'user': session['user'],
            'payment': payment,
            'language': language,
            'date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        orders = load_json('data/orders.json')
        orders.append(order)
        save_json('data/orders.json', orders)
        # persist this order in session
        session['order'] = order
        session.pop('cart', None)
        # redirect to bill page after order creation
        return redirect(url_for('bill', order_id=order_id))
    return render_template('checkout.html', cart=session.get('cart', []))

@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.get_json()
    cart = data['cart']
    total = data['total']
    table_no = data['table']
    payment = data['payment']
    language = data.get('language')
    order_id = str(uuid.uuid4())[:8]
    order = {
        'id': order_id,
        'table': table_no,
        'order_items': cart,
        'total': total,
        'user': session.get('user', 'Guest'),
        'payment': payment,
        'language': language,
        'date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    session['order'] = order
    orders = load_json('data/orders.json')
    orders.append(order)
    save_json('data/orders.json', orders)
    # ✅ Clear cart after successful order
    session.pop("cart", None)
    return jsonify({
        "success": True,
        "order_id": order_id
    })

@app.route('/bill/<order_id>')
def bill(order_id):
    orders = load_json("data/orders.json")
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        return 'Order not found', 404
    return render_template('bill.html', order=order)

@app.route('/generate_bill/<order_id>')
def generate_bill(order_id):
    orders = load_json("data/orders.json")
    order = next((o for o in orders if o.get("id") == order_id), None)
    if not order:
        return 'Order not found', 404

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Shiv Shambhu Hotel - Godavari Complex, Kopargaon", ln=True, align="C")
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Order ID: {order.get('id', '')}", ln=True)
    pdf.cell(0, 8, f"Table Number: {order.get('table', '')}", ln=True)
    pdf.cell(0, 8, f"Payment Method: {order.get('payment', '')}", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(120, 8, "Item Name", border=1)
    pdf.cell(50, 8, "Price", border=1, ln=True)

    pdf.set_font("Helvetica", "", 12)
    items = order.get("order_items", [])
    for item in items:
        name = item.get("name", "")
        price = item.get("price", 0)
        pdf.cell(120, 8, str(name), border=1)
        pdf.cell(50, 8, f"Rs {price}", border=1, ln=True)

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, f"Total Amount Paid: Rs {order.get('total', 0)}", ln=True)

    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="Shiv_Shambhu_Bill.pdf"
    )

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/admin-register', methods=['GET', 'POST'])
def admin_register():
    admin_file = 'data/admin.json'
    if os.path.exists(admin_file):
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin_data = {'username': username, 'password': password}
        save_json(admin_file, admin_data)
        return redirect(url_for('admin_login'))
    return render_template('admin_register.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    admin_file = 'data/admin.json'
    if not os.path.exists(admin_file):
        return redirect(url_for('admin_register'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin_data = load_json(admin_file)
        if admin_data.get('username') == username and admin_data.get('password') == password:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        return 'Invalid credentials', 400
    return render_template('admin_login.html')

@app.route('/admin')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    orders_normalized = [normalize_order(o) for o in load_json('data/orders.json')]
    return render_template('admin_dashboard.html', orders=orders_normalized)

@app.route('/admin/complete/<order_id>', methods=['GET', 'POST'])
def complete_order(order_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    orders = load_json("data/orders.json")

    order_to_complete = None
    for o in orders:
        oid = o.get("id") or o.get("order_id")
        if oid == order_id:
            order_to_complete = o
            break

    if order_to_complete:
        orders.remove(order_to_complete)
        save_json("data/orders.json", orders)

        history = load_json("data/history.json")
        history.append(order_to_complete)
        save_json("data/history.json", history)

    return redirect(url_for("admin_dashboard"))

@app.route('/admin/history')
def admin_history():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    history_normalized = [normalize_order(o) for o in load_json(HISTORY_FILE)]
    today = datetime.now().strftime('%Y-%m-%d')
    today_orders = [
        o for o in history_normalized
        if o.get("date_time") and o["date_time"].startswith(today)
    ]
    cash_total = sum(o['total'] for o in today_orders if o['payment_method'] == 'cash')
    upi_total = sum(o['total'] for o in today_orders if o['payment_method'] == 'upi')
    total_revenue = cash_total + upi_total
    return render_template('admin_history.html', orders=today_orders, total_revenue=total_revenue, cash_revenue=cash_total, upi_revenue=upi_total, show_10_days=False)

@app.route("/admin/history/reset")
def reset_history():
    history = load_json("data/history.json")
    history = history if history else []
    today = datetime.now().strftime("%Y-%m-%d")
    # Remove ONLY today's orders
    history = [
        o for o in history
        if not (o.get("date_time") and o["date_time"].startswith(today))
    ]
    # Save back remaining old history (last 10 days stays)
    save_json("data/history.json", history)
    return redirect(url_for("admin_history"))

@app.route("/admin/history/10days")
def history_10days():
    history = load_json("data/history.json")

    cutoff = datetime.now() - timedelta(days=10)

    ten_days_orders = []
    total_cash = 0
    total_upi = 0

    for o in history:
        dt = o.get("date_time","")
        if dt:
            order_date = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
            if order_date >= cutoff:
                ten_days_orders.append(o)

                if o.get("payment") == "Cash":
                    total_cash += o.get("total",0)
                elif o.get("payment") == "UPI":
                    total_upi += o.get("total",0)

    return render_template(
        "admin_history.html",
        orders=ten_days_orders,
        cash_revenue=total_cash,
        upi_revenue=total_upi,
        total_revenue=total_cash+total_upi,
        show_10_days=True
    )

@app.route('/admin-logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
