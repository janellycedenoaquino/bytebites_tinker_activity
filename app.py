import streamlit as st
from decimal import Decimal
from datetime import datetime
from models import FoodItem, Menu

st.set_page_config(page_title="ByteBites", page_icon="🌿", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #1E1E1E;
    color: #EBEBEB;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1100px; margin: auto; }

/* ─── Header ─── */
.bb-header {
    background: #252525;
    border-radius: 20px 20px 0 0;
    padding: 3rem 3rem 2rem;
    margin-bottom: 0;
    position: relative;
    overflow: hidden;
    border-bottom: 3px solid #C4704A;
}
.bb-header-deco {
    position: absolute;
    right: 3rem; top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    opacity: 0.15;
    line-height: 1;
}
.bb-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3.8rem;
    font-weight: 900;
    color: #C4704A;
    margin: 0 0 0.2rem;
    letter-spacing: -0.02em;
    line-height: 1;
}
.bb-header h1 span { color: #5C7A5C; }
.bb-header p {
    font-size: 0.88rem;
    color: #9A9A9A;
    margin: 0.5rem 0 0;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ─── Section labels ─── */
.bb-section-label {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #C4704A;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.bb-section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #3A3A3A;
    margin-left: 0.5rem;
}

/* ─── Cards ─── */
.bb-card {
    background: #2A2A2A;
    border: 1px solid #3A3A3A;
    border-radius: 16px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 0.8rem;
    transition: box-shadow 0.2s, border-color 0.2s;
}
.bb-card:hover {
    box-shadow: 0 4px 20px rgba(196,112,74,0.15);
    border-color: #C4704A;
}
.bb-card-title {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 1.05rem;
    color: #EBEBEB;
    margin-bottom: 0.3rem;
}
.bb-card-meta { font-size: 0.82rem; color: #9A9A9A; font-weight: 500; }

.bb-badge {
    display: inline-block;
    border-radius: 4px;
    padding: 0.15rem 0.65rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.05em;
    margin-right: 0.35rem;
    background: #3A2A20;
    color: #C4704A;
    font-weight: 500;
}

.bb-price {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #5C7A5C;
}

/* ─── Order box ─── */
.bb-order-box {
    background: #2A2A2A;
    border: 1px solid #3A3A3A;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.bb-order-row {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px dashed #3A3A3A;
    font-size: 0.9rem;
    font-weight: 500;
}
.bb-order-total {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 900;
    color: #C4704A;
    text-align: right;
    margin-top: 1rem;
}

/* ─── Inputs ─── */
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] select,
div[data-testid="stNumberInput"] input {
    background: #2A2A2A !important;
    border: 1.5px solid #3A3A3A !important;
    border-radius: 10px !important;
    color: #EBEBEB !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #C4704A !important;
    box-shadow: 0 0 0 3px rgba(196,112,74,0.12) !important;
}

/* ─── Buttons ─── */
div[data-testid="stButton"] > button {
    background: #C4704A !important;
    color: #FAF7F2 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    transition: background 0.2s !important;
}
div[data-testid="stButton"] > button:hover { background: #A85A3A !important; }

.bb-divider { border: none; height: 1px; background: #3A3A3A; margin: 1.5rem 0; }
.bb-dots { color: #C4704A; font-size: 0.85rem; letter-spacing: 0.05em; }
</style>
""", unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────

def init_state():
    if "menu" not in st.session_state:
        menu = Menu()
        for item in [
            FoodItem("Spicy Burger",         Decimal("8.99"), "Burgers",  4.8),
            FoodItem("Classic Cheeseburger", Decimal("7.49"), "Burgers",  4.5),
            FoodItem("Mushroom Swiss",       Decimal("8.49"), "Burgers",  4.2),
            FoodItem("Large Soda",           Decimal("2.49"), "Drinks",   4.6),
            FoodItem("Mango Smoothie",       Decimal("4.99"), "Drinks",   4.9),
            FoodItem("Iced Matcha Latte",    Decimal("5.49"), "Drinks",   4.7),
            FoodItem("Churro Bites",         Decimal("3.99"), "Desserts", 4.8),
            FoodItem("Strawberry Crepe",     Decimal("5.99"), "Desserts", 4.6),
            FoodItem("Mochi Ice Cream",      Decimal("4.49"), "Desserts", 4.9),
            FoodItem("Loaded Fries",         Decimal("4.29"), "Sides",    4.4),
            FoodItem("Onion Rings",          Decimal("3.49"), "Sides",    4.1),
            FoodItem("Mini Corn Dogs",       Decimal("3.99"), "Snacks",   4.3),
        ]:
            menu.add_item(item)
        st.session_state.menu = menu
    if "cart" not in st.session_state:
        st.session_state.cart = {}  # {FoodItem: qty}
    if "orders" not in st.session_state:
        st.session_state.orders = []
    if "last_order_name" not in st.session_state:
        st.session_state.last_order_name = None

init_state()

CATEGORIES = ["Burgers", "Drinks", "Desserts", "Snacks", "Sides"]

def rating_dots(item):
    filled = int(round(item.get_popularity_rating()))
    return "●" * filled + "○" * (5 - filled)


# ── 1. Header ─────────────────────────────────────────────────────────────────

st.markdown("""
<div class="bb-header">
    <div class="bb-header-deco">🌿🍋🫙</div>
    <h1>Byte<span>Bites</span></h1>
    <p>Fresh · Fast · Digital</p>
</div>
""", unsafe_allow_html=True)


# ── 2. Category filter bar ────────────────────────────────────────────────────

selected_cat = st.selectbox("Browse by category", ["All"] + CATEGORIES)


# ── 3. Two-column layout ──────────────────────────────────────────────────────

left, right = st.columns([2, 1])

# LEFT — Menu Grid
with left:
    st.markdown('<div class="bb-section-label">Our Offerings</div>', unsafe_allow_html=True)
    items = (
        st.session_state.menu.get_all_items()
        if selected_cat == "All"
        else st.session_state.menu.filter_by_category(selected_cat)
    )
    grid = st.columns(3)
    for i, item in enumerate(items):
        with grid[i % 3]:
            st.markdown(f"""
            <div class="bb-card" style="padding:0.8rem 1rem;margin-bottom:0.5rem;">
                <span class="bb-badge">{item.get_category()}</span>
                <div style="margin-top:0.5rem;">
                    <div class="bb-card-title" style="font-size:0.9rem;">{item.get_name()}</div>
                    <div class="bb-price" style="font-size:1rem;">${item.get_price()}</div>
                    <div class="bb-dots" style="margin-top:0.2rem;font-size:0.7rem;">{rating_dots(item)}
                        <span style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#9A8070;">
                            {item.get_popularity_rating()}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Add to Order", key=f"add_{item.get_name()}"):
                st.session_state.cart[item] = st.session_state.cart.get(item, 0) + 1

# RIGHT — Order Panel
with right:
    st.markdown('<div class="bb-section-label">Your Order</div>', unsafe_allow_html=True)

    if st.session_state.last_order_name:
        st.success(f"Order placed! Thanks, {st.session_state.last_order_name}!")
        st.session_state.last_order_name = None

    cart = st.session_state.cart
    if not cart:
        st.markdown("""
        <div style="text-align:center;padding:2.5rem 1rem;">
            <div style="font-size:2.5rem;">🍽️</div>
            <div style="color:#C4704A;opacity:0.8;font-weight:600;font-family:'DM Sans',sans-serif;margin:0.6rem 0 0.3rem;">
                Your order is empty
            </div>
            <div style="font-size:0.82rem;color:#888888;">
                Add something delicious to get started.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        total = Decimal("0")
        order_html = '<div class="bb-order-box">'
        for fi, qty in cart.items():
            line = fi.get_price() * qty
            total += line
            order_html += f'<div class="bb-order-row"><span style="color:#EBEBEB;">{fi.get_name()} × {qty}</span><span class="bb-price">${line}</span></div>'
        order_html += f'<div style="display:flex;justify-content:space-between;padding:0.6rem 0 0;font-size:0.85rem;font-weight:500;"><span style="color:#888888;">Subtotal</span><span style="color:#888888;">${total}</span></div>'
        order_html += f'<div class="bb-order-total">Total: ${total}</div>'
        order_html += '</div>'
        st.markdown(order_html, unsafe_allow_html=True)

        name = st.text_input("Your name", placeholder="Enter your name to place order")
        if st.button("Place Order"):
            if not name.strip():
                st.warning("Please enter your name to place the order.")
            else:
                st.session_state.orders.append({
                    "customer": name.strip(),
                    "items": [(fi.get_name(), qty) for fi, qty in cart.items()],
                    "total": total,
                    "timestamp": datetime.now().strftime("%b %d, %Y · %H:%M"),
                })
                st.session_state.cart = {}
                st.session_state.last_order_name = name.strip()
                st.rerun()


# ── 4. Add to Menu ────────────────────────────────────────────────────────────

st.markdown('<hr class="bb-divider">', unsafe_allow_html=True)
with st.expander("＋ Add a new item to the menu"):
    c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1])
    with c1: iname = st.text_input("Item name", placeholder="Name", key="new_name")
    with c2: iprice = st.number_input("Price", min_value=0.0, step=0.5, format="%.2f", key="new_price")
    with c3: icat = st.selectbox("Category", CATEGORIES, key="new_cat")
    with c4: ipop = st.slider("Rating", 1.0, 5.0, 4.0, 0.1, key="new_rating")
    with c5:
        st.write("")
        if st.button("Add Item"):
            if iname.strip():
                added = st.session_state.menu.add_item(
                    FoodItem(iname.strip(), Decimal(str(iprice)), icat, ipop)
                )
                if added:
                    st.success("Added!")
                else:
                    st.warning("An item with that name already exists.")
            else:
                st.warning("Please enter an item name.")


# ── 5. Top Picks ──────────────────────────────────────────────────────────────

st.markdown('<div class="bb-section-label" style="margin-top:1.5rem;">Top Picks</div>', unsafe_allow_html=True)
top_items = sorted(
    st.session_state.menu.get_all_items(),
    key=lambda x: x.get_popularity_rating(),
    reverse=True
)[:5]
cards_html = "".join(f'<div style="min-width:160px;flex-shrink:0;background:#2A2A2A;border:1px solid #3A3A3A;border-radius:16px;padding:1.2rem;"><div style="font-family:\'Playfair Display\',serif;font-size:1.4rem;font-weight:900;color:#3A3A3A;">0{rank}</div><div style="font-family:\'Playfair Display\',serif;font-weight:700;font-size:1rem;color:#EBEBEB;margin:0.4rem 0 0.2rem;">{item.get_name()}</div><div style="font-family:\'Playfair Display\',serif;font-weight:700;color:#5C7A5C;">${item.get_price()}</div><div class="bb-dots" style="margin-top:0.3rem;">{rating_dots(item)}</div></div>' for rank, item in enumerate(top_items, 1))
st.markdown(
    f'<div style="display:flex;overflow-x:auto;gap:16px;padding-bottom:0.5rem;">{cards_html}</div>',
    unsafe_allow_html=True
)


# ── 6. Previous Orders ────────────────────────────────────────────────────────

st.markdown('<hr class="bb-divider">', unsafe_allow_html=True)
st.markdown('<div class="bb-section-label">Previous Orders</div>', unsafe_allow_html=True)

if not st.session_state.orders:
    st.markdown(
        '<p style="color:#888888;font-style:italic;">No orders placed yet.</p>',
        unsafe_allow_html=True
    )
else:
    for order in reversed(st.session_state.orders):
        items_str = ", ".join(f"{n} ×{q}" for n, q in order["items"])
        st.markdown(f"""
        <div class="bb-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                    <div class="bb-card-title">{order["customer"]}</div>
                    <div class="bb-card-meta" style="margin-top:0.3rem;">{items_str}</div>
                </div>
                <div style="text-align:right;">
                    <div class="bb-price">${order["total"]}</div>
                    <div class="bb-card-meta">{order["timestamp"]}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
