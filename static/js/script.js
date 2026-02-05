const translations = {
    en: {
        nav_menu: "Menu",
        nav_about: "About Us",
        nav_contact: "Contact Us",
        settings: "Settings",
        language: "Language",
        logout: "Logout",
        hero_title: "Delicious Food Delivered Fresh",
        hero_subtitle: "Experience authentic flavors crafted with love and tradition.",
        cta_explore: "Explore Menu",
        cat_breakfast: "Breakfast",
        cat_lunch: "Lunch",
        cat_beverages: "Beverages",
        cat_dinner: "Dinner",
        welcome: "Welcome",
        add_plus: "Add +",
        checkout_title: "Checkout",
        your_order: "Your Order",
        total_label: "Total",
        table_number: "Table Number:",
        payment_method: "Payment Method:",
        done: "Done",
        your_cart: "Your Cart",
        order_summary: "Order Summary",
        dish: "Dish",
        subtotal: "Subtotal",
        shipping: "Shipping",
        free: "Free",
        tax: "Tax",
        secure_checkout: "Secure Checkout",
        order_success: "Order Successfully Placed!",
        order_id: "Order ID",
        download_bill: "Download Bill"
    },
    hi: {
        nav_menu: "मेनू",
        nav_about: "हमारे बारे में",
        nav_contact: "संपर्क करें",
        settings: "सेटिंग्स",
        language: "भाषा",
        logout: "लॉगआउट",
        hero_title: "स्वादिष्ट भोजन ताज़ा परोसा जाता है",
        hero_subtitle: "पारंपरिक स्वाद और प्यार से बनी रेसिपी का आनंद लें।",
        cta_explore: "मेनू देखें",
        cat_breakfast: "नाश्ता",
        cat_lunch: "दोपहर का भोजन",
        cat_beverages: "पेय",
        cat_dinner: "रात का भोजन",
        welcome: "स्वागत",
        add_plus: "जोड़ें +",
        checkout_title: "चेकआउट",
        your_order: "आपका ऑर्डर",
        total_label: "कुल",
        table_number: "टेबल नंबर:",
        payment_method: "भुगतान विधि:",
        done: "पूर्ण",
        your_cart: "आपकी कार्ट",
        order_summary: "ऑर्डर सारांश",
        dish: "डिश",
        subtotal: "उप-योग",
        shipping: "डिलीवरी",
        free: "मुफ्त",
        tax: "कर",
        secure_checkout: "सुरक्षित चेकआउट",
        order_success: "ऑर्डर सफलतापूर्वक हो गया!",
        order_id: "ऑर्डर आईडी",
        download_bill: "बिल डाउनलोड करें"
    },
    mr: {
        nav_menu: "मेनू",
        nav_about: "आमच्याबद्दल",
        nav_contact: "संपर्क",
        settings: "सेटिंग्ज",
        language: "भाषा",
        logout: "लॉगआउट",
        hero_title: "ताजे आणि चविष्ट पदार्थ",
        hero_subtitle: "प्रेम आणि परंपरेने तयार केलेले खास स्वाद.",
        cta_explore: "मेनू पहा",
        cat_breakfast: "नाश्ता",
        cat_lunch: "दुपारचे जेवण",
        cat_beverages: "पेय",
        cat_dinner: "रात्रीचे जेवण",
        welcome: "स्वागत",
        add_plus: "जोडा +",
        checkout_title: "चेकआउट",
        your_order: "तुमची ऑर्डर",
        total_label: "एकूण",
        table_number: "टेबल क्रमांक:",
        payment_method: "पेमेंट पद्धत:",
        done: "पूर्ण",
        your_cart: "तुमची कार्ट",
        order_summary: "ऑर्डर सारांश",
        dish: "डिश",
        subtotal: "उप-एकूण",
        shipping: "डिलिव्हरी",
        free: "मोफत",
        tax: "कर",
        secure_checkout: "सुरक्षित चेकआउट",
        order_success: "ऑर्डर यशस्वी!",
        order_id: "ऑर्डर आयडी",
        download_bill: "बिल डाउनलोड करा"
    }
};

function getCurrentLanguage() {
    return localStorage.getItem('language') || 'en';
}

function applyTranslations(lang) {
    const strings = translations[lang] || translations.en;
    document.documentElement.lang = lang;

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (strings[key]) {
            el.textContent = strings[key];
        }
    });

    document.querySelectorAll('input[name="language"]').forEach(input => {
        input.value = lang;
    });

    document.querySelectorAll('.lang-option').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
    });
}

function changeLanguage(lang) {
    localStorage.setItem('language', lang);
    applyTranslations(lang);
}

function t(key) {
    const lang = getCurrentLanguage();
    if (translations[lang] && translations[lang][key]) {
        return translations[lang][key];
    }
    return (translations.en && translations.en[key]) ? translations.en[key] : key;
}

function setupLanguageMenu() {
    const languageDropdown = document.getElementById('language-dropdown');
    const languageTrigger = document.getElementById('language-trigger');
    const settingsMenu = document.getElementById('settings-menu');

    if (languageTrigger && languageDropdown) {
        languageTrigger.addEventListener('click', function(e) {
            e.stopPropagation();
            languageDropdown.classList.toggle('open');
        });
    }

    document.querySelectorAll('.lang-option').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            changeLanguage(this.getAttribute('data-lang'));
            if (languageDropdown) {
                languageDropdown.classList.remove('open');
            }
        });
    });

    if (settingsMenu) {
        settingsMenu.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }

    document.addEventListener('click', function() {
        if (languageDropdown) {
            languageDropdown.classList.remove('open');
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    applyTranslations(getCurrentLanguage());
    setupLanguageMenu();
    loadCart();
    setupCategoryFilters();
    setupCTAButton();
    setupSuccessModal();
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

function setupSuccessModal() {
    const modal = document.getElementById('success-modal');
    if (!modal) return;

    const closeBtn = document.getElementById('success-close');
    const downloadBtn = document.getElementById('download-bill-btn');

    if (closeBtn) {
        closeBtn.addEventListener('click', closeSuccessModal);
    }

    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeSuccessModal();
        }
    });

    if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
            const orderId = downloadBtn.getAttribute('data-order-id');
            if (orderId) {
                window.location.href = `/generate_bill/${orderId}`;
            }
        });
    }
}

function openSuccessModal(orderId) {
    const modal = document.getElementById('success-modal');
    const orderIdEl = document.getElementById('success-order-id');
    const downloadBtn = document.getElementById('download-bill-btn');
    if (!modal) return;

    if (orderIdEl) orderIdEl.textContent = orderId;
    if (downloadBtn) downloadBtn.setAttribute('data-order-id', orderId);
    modal.classList.add('active');
    modal.setAttribute('aria-hidden', 'false');
}

function closeSuccessModal() {
    const modal = document.getElementById('success-modal');
    if (!modal) return;
    modal.classList.remove('active');
    modal.setAttribute('aria-hidden', 'true');
}

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
                    <div class="cart-item-category">${t('dish')}</div>
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
        const languageField = document.getElementById('language-field');
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
        if (languageField) {
            languageField.value = getCurrentLanguage();
        }
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
    const language = getCurrentLanguage();

    if (!tableNo || !payment || !cartData || !totalData) {
        alert('Please fill all fields');
        return;
    }

    const data = {
        cart: JSON.parse(cartData),
        total: parseFloat(totalData),
        table: tableNo,
        payment: payment,
        language: language
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
            openSuccessModal(data.order_id);
            loadCart();
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
