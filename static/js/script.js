document.addEventListener('DOMContentLoaded', function() {
    loadCart();
    setupCategoryFilters();
    setupCTAButton();
    const cartIcon = document.getElementById('cart-icon');
    if (cartIcon) cartIcon.addEventListener('click', openCart);

    // Add event listener for UPI QR code display and payment option visuals
    document.querySelectorAll('input[name="payment"]').forEach(radio => {
        radio.addEventListener('change', function() {
            const qrCode = document.getElementById('qr-code');
            if (qrCode) {
                qrCode.style.display = this.value === 'UPI' ? 'block' : 'none';
            }

            // Add selected class to the parent payment-option if exists
            document.querySelectorAll('.payment-option').forEach(option => option.classList.remove('selected'));
            if (this.closest && this.closest('.payment-option')) {
                this.closest('.payment-option').classList.add('selected');
            }
        });
    });
    // Event delegation for add buttons (uses data attributes to avoid inline JS with Jinja)
    document.body.addEventListener('click', function(e) {
        const btn = e.target.closest && e.target.closest('.add-btn');
        if (btn) {
            const name = btn.getAttribute('data-name');
            const price = parseFloat(btn.getAttribute('data-price')) || 0;
            addToCart(name, price);
        }
    });
});

function addToCart(name, price) {
    fetch('/add_to_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name, price: price }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'added') {
            loadCart();
        }
    });
}

function removeFromCart(name) {
    fetch('/remove_from_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'removed') {
            loadCart();
        }
    });
}

function loadCart() {
    fetch('/get_cart')
    .then(response => response.json())
    .then(cart => {
        const cartList = document.getElementById('cart-list');
        const totalSpan = document.getElementById('total');
        const subtotalSpan = document.getElementById('subtotal');
        const taxSpan = document.getElementById('tax');
        const cartCount = document.getElementById('cart-count');
        const checkoutBtn = document.getElementById('checkout-btn');
        cartList.innerHTML = '';
        let total = 0;
        let itemCount = 0;

        // Group items by name
        const groupedCart = {};
        cart.forEach(item => {
            if (!groupedCart[item.name]) {
                groupedCart[item.name] = { name: item.name, price: item.price, quantity: 0, image: getItemImage(item.name) };
            }
            groupedCart[item.name].quantity += 1;
            total += item.price;
            itemCount += 1;
        });

        // Render each unique item
        Object.values(groupedCart).forEach(item => {
            const card = document.createElement('div');
            card.className = 'cart-item-card';
            card.innerHTML = `
                <img src="${item.image}" alt="${item.name}" class="cart-item-image">
                <div class="cart-item-details">
                    <div class="cart-item-name">${item.name}</div>
                    <div class="cart-item-category">Dish</div>
                    <div class="quantity-controls">
                        <button class="quantity-btn" onclick="changeQuantity('${item.name}', -1)">-</button>
                        <span class="quantity-display">${item.quantity}</span>
                        <button class="quantity-btn" onclick="changeQuantity('${item.name}', 1)">+</button>
                    </div>
                    <div class="cart-item-price">₹${item.price * item.quantity}</div>
                </div>
                <button class="remove-btn" onclick="removeAllFromCart('${item.name}')">×</button>
            `;
            cartList.appendChild(card);
        });

        totalSpan.textContent = '₹' + total;
        if (subtotalSpan) subtotalSpan.textContent = '₹' + total;
        if (taxSpan) taxSpan.textContent = '₹0';
        if (cartCount) {
            cartCount.textContent = itemCount;
        }
        if (checkoutBtn) {
            checkoutBtn.style.display = itemCount > 0 ? 'block' : 'none';
        }
    });
}

function getItemImage(name) {
    // Map item names to images from menu cards
    const menuCards = document.querySelectorAll('.menu-card');
    for (let card of menuCards) {
        const cardName = card.querySelector('h4').textContent.trim();
        if (cardName === name) {
            return card.querySelector('img').src;
        }
    }
    return 'https://via.placeholder.com/80x80?text=Food'; // Placeholder
}

function changeQuantity(name, delta) {
    if (delta > 0) {
        // Add one
        const price = getItemPrice(name);
        addToCart(name, price);
    } else if (delta < 0) {
        // Remove one
        removeFromCart(name);
    }
}

function removeAllFromCart(name) {
    // Remove all instances
    fetch('/get_cart')
    .then(response => response.json())
    .then(cart => {
        const count = cart.filter(item => item.name === name).length;
        for (let i = 0; i < count; i++) {
            removeFromCart(name);
        }
    });
}

function getItemPrice(name) {
    const menuCards = document.querySelectorAll('.menu-card');
    for (let card of menuCards) {
        const cardName = card.querySelector('h4').textContent.trim();
        if (cardName === name) {
            const priceText = card.querySelector('p').textContent.trim();
            return parseInt(priceText.replace('₹', ''));
        }
    }
    return 0;
}

function proceedToCheckout() {
    // Hide menu and show checkout
    document.getElementById('menu-container').style.display = 'none';
    document.getElementById('checkout-section').style.display = 'block';
    document.getElementById('cartSidebar').classList.remove('active');

    // Load cart into checkout
    fetch('/get_cart')
    .then(response => response.json())
    .then(cart => {
        const checkoutCartList = document.getElementById('checkout-cart-list');
        const checkoutTotal = document.getElementById('checkout-total');
        const cartData = document.getElementById('cart-data');
        const totalData = document.getElementById('total-data');
        checkoutCartList.innerHTML = '';
        let total = 0;
        cart.forEach(item => {
            const li = document.createElement('li');
            li.innerHTML = `${item.name} - ₹${item.price}`;
            checkoutCartList.appendChild(li);
            total += item.price;
        });
        checkoutTotal.textContent = total;
        cartData.value = JSON.stringify(cart);
        totalData.value = total;
    });
}

function submitOrder() {
    const tableEl = document.getElementById('table_no');
    const tableNo = tableEl ? tableEl.value : null;
    const paymentEl = document.querySelector('input[name="payment"]:checked');
    const payment = paymentEl ? paymentEl.value : null;
    const cartDataEl = document.getElementById('cart-data');
    const totalDataEl = document.getElementById('total-data');
    const cartData = cartDataEl ? cartDataEl.value : null;
    const totalData = totalDataEl ? totalDataEl.value : null;

    if (!tableNo || !payment || !cartData || !totalData) {
        alert('Please fill all fields');
        return;
    }

    const data = {
        cart: JSON.parse(cartData),
        total: parseFloat(totalData),
        table: tableNo,
        payment: payment
    };

    fetch('/place_order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.order_id) {
            alert('Order placed — ID: ' + data.order_id);
            // go back to menu/home
            window.location.href = '/menu';
        } else {
            alert('Error submitting order');
        }
    })
    .catch(error => {
        console.error(error);
        alert('Error submitting order. Check console for details.');
    });
}

// helper: change quantity (add or remove single item)

function openCart() {
    document.getElementById("cartSidebar").classList.add("active");
}

function closeCart() {
    document.getElementById("cartSidebar").classList.remove("active");
}

function setupCategoryFilters() {
    const categoryIcons = document.querySelectorAll('.category-icon');
    const menuCategories = document.querySelectorAll('.menu-category');

    categoryIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            filterMenuByCategory(category);
        });
    });
}

function filterMenuByCategory(category) {
    const menuCategories = document.querySelectorAll('.menu-category');
    menuCategories.forEach(cat => {
        if (category === 'ALL' || cat.querySelector('h3').textContent.toUpperCase() === category) {
            cat.style.display = 'block';
        } else {
            cat.style.display = 'none';
        }
    });
}

function setupCTAButton() {
    const ctaButton = document.querySelector('.cta-button');
    if (ctaButton) {
        ctaButton.addEventListener('click', function() {
            const menuSection = document.querySelector('.categories');
            if (menuSection) {
                menuSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }
}
