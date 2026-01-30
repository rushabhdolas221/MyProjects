import streamlit as st
import pandas as pd
import os
import qrcode
import io

# ================== CONFIG ==================
st.set_page_config(page_title="One For All", layout="wide")

ADMIN_MOBILE = "9325048812"
ADMIN_PASSWORD = "Rushabh@1805"
USERS_FILE = "users.csv"
ASSETS = "assets"

# ================== INIT USER DB ==================
if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["mobile", "flat"]).to_csv(USERS_FILE, index=False)

# ================== SESSION STATE ==================
defaults = {
    "page": "welcome",
    "role": None,
    "logged_in": False,
    "mobile": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ================== PROPERTY DATA (DEMO DB) ==================
if "properties" not in st.session_state:
    st.session_state.properties = [
        {"flat": "101", "status": "Rented", "tenant": "Rahul", "rent": 12000, "rent_requested": True},
        {"flat": "102", "status": "Vacant", "tenant": None, "rent": 10000, "rent_requested": False},
        {"flat": "103", "status": "Vacant", "tenant": None, "rent": 9000, "rent_requested": False},
    ]

# ================== LOCATIONS ==================
LOCATIONS = {
    "Home": (12.9279, 77.6271),
    "Office": (12.9352, 77.6245),
    "College": (12.9716, 77.5946),
}

# ================== WELCOME PAGE ==================
def welcome():
    st.title("One For All")
    st.caption("Unified Housing • Travel • Local Services Platform")
    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        st.image(f"{ASSETS}/user.png", width=120)
        if st.button("User Login / Register"):
            st.session_state.role = "user"
            st.session_state.page = "user_login"

    with c2:
        st.image(f"{ASSETS}/admin.png", width=120)
        if st.button("Admin Login"):
            st.session_state.role = "admin"
            st.session_state.page = "admin_login"

# ================== USER LOGIN ==================
def user_login():
    st.title("User Login")
    mobile = st.text_input("Mobile Number")

    if st.button("Login"):
        st.session_state.logged_in = True
        st.session_state.mobile = mobile
        st.session_state.page = "user_dashboard"

# ================== ADMIN LOGIN ==================
def admin_login():
    st.title("Admin Login")
    mobile = st.text_input("Admin Mobile")
    password = st.text_input("Password", type="password")

    st.info("Admin account is predefined")

    if st.button("Login"):
        if mobile == ADMIN_MOBILE and password == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.session_state.page = "admin_dashboard"
        else:
            st.error("Invalid admin credentials")

# ================== USER DASHBOARD ==================
def user_dashboard():
    st.title("User Dashboard")
    st.caption(f"Logged in as: {st.session_state.mobile}")
    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.image(f"{ASSETS}/rent.png", width=70)
        if st.button("Pay Rent"):
            st.session_state.page = "pay_rent"

    with c2:
        st.image(f"{ASSETS}/ride.png", width=70)
        if st.button("Book Ride"):
            st.session_state.page = "book_ride"

    with c3:
        st.image(f"{ASSETS}/services.png", width=70)
        if st.button("Local Services"):
            st.session_state.page = "services"

    with c4:
        if st.button("Browse Flats"):
            st.session_state.page = "browse_flats"

    if st.button("Logout"):
        reset()

# ================== BROWSE FLATS ==================
def browse_flats():
    st.title("Available Flats for Rent")
    st.divider()

    for p in st.session_state.properties:
        if p["status"] == "Vacant":
            col1, col2, col3 = st.columns([1,2,1])
            col1.write(f"Flat {p['flat']}")
            col2.write(f"Rent: ₹{p['rent']}")
            if col3.button("Request Flat", key=p["flat"]):
                p["status"] = "Requested"
                p["tenant"] = st.session_state.mobile
                st.success(f"Request sent for Flat {p['flat']}")

    if st.button("Back"):
        st.session_state.page = "user_dashboard"

# ================== PAY RENT ==================
def pay_rent():
    st.title("Pay Rent")
    st.divider()

    flat = next((p for p in st.session_state.properties if p["tenant"] == st.session_state.mobile), None)

    if flat and flat["rent_requested"]:
        qr = qrcode.make(f"upi://pay?pa=owner@upi&am={flat['rent']}")
        buf = io.BytesIO()
        qr.save(buf)
        st.image(buf.getvalue(), width=250)

        if st.button("Payment Successful"):
            flat["rent_requested"] = False
            st.success("Rent paid successfully")
    else:
        st.info("No rent due currently")

    if st.button("Back"):
        st.session_state.page = "user_dashboard"

# ================== BOOK RIDE ==================
def book_ride():
    st.title("Book Ride")
    pickup = st.selectbox("Pickup", list(LOCATIONS.keys()))
    drop = st.selectbox("Drop", list(LOCATIONS.keys()))

    df = pd.DataFrame({
        "lat": [LOCATIONS[pickup][0], LOCATIONS[drop][0]],
        "lon": [LOCATIONS[pickup][1], LOCATIONS[drop][1]],
    })
    st.map(df)
    st.success("Ride booking simulated")

    if st.button("Back"):
        st.session_state.page = "user_dashboard"

# ================== LOCAL SERVICES ==================
def services():
    st.title("Local Services")
    st.divider()

    workers = [
        ("Ramesh", "Plumber", "plumber.png", 300),
        ("Suresh", "Electrician", "electrician.png", 350),
        ("Lakshmi", "Maid", "maid.png", 250),
        ("Anita", "Cleaner", "cleaner.png", 280),
    ]

    for n, r, img, p in workers:
        col1, col2, col3 = st.columns([1,3,1])
        col1.image(f"{ASSETS}/{img}", width=70)
        col2.write(f"**{n}** – {r} – ₹{p}")
        col3.button("Book", key=n)

    if st.button("Back"):
        st.session_state.page = "user_dashboard"

# ================== ADMIN DASHBOARD ==================
def admin_dashboard():
    st.title("Admin Dashboard")
    st.caption("Property, Tenant & Rent Management")
    st.divider()

    props = st.session_state.properties

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Flats", len(props))
    c2.metric("Rented", len([p for p in props if p["status"] == "Rented"]))
    c3.metric("Vacant", len([p for p in props if p["status"] == "Vacant"]))

    st.subheader("Properties")

    for p in props:
        col1, col2, col3, col4 = st.columns([1,2,2,2])
        col1.write(f"Flat {p['flat']}")
        col2.write(p["status"])
        col3.write(p["tenant"] if p["tenant"] else "-")

        if p["status"] in ["Rented", "Requested"]:
            if col4.button("Send Rent Request", key=f"rent{p['flat']}"):
                p["rent_requested"] = True
                p["status"] = "Rented"
                st.success(f"Rent request sent for Flat {p['flat']}")

    st.subheader("Add New Flat")
    new_flat = st.text_input("Flat Number")
    rent = st.number_input("Monthly Rent", step=500)
    if st.button("Add Flat"):
        st.session_state.properties.append(
            {"flat": new_flat, "status": "Vacant", "tenant": None, "rent": rent, "rent_requested": False}
        )
        st.success("Flat added")

    if st.button("Logout"):
        reset()

# ================== RESET ==================
def reset():
    st.session_state.clear()
    st.rerun()

# ================== ROUTER ==================
if st.session_state.page == "welcome":
    welcome()
elif st.session_state.page == "user_login":
    user_login()
elif st.session_state.page == "admin_login":
    admin_login()
elif st.session_state.page == "user_dashboard":
    user_dashboard()
elif st.session_state.page == "browse_flats":
    browse_flats()
elif st.session_state.page == "pay_rent":
    pay_rent()
elif st.session_state.page == "book_ride":
    book_ride()
elif st.session_state.page == "services":
    services()
elif st.session_state.page == "admin_dashboard":
    admin_dashboard()
