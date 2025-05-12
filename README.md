# 🧾 Online Auction System

An online auction platform built with **Django** that enables sellers to list products, buyers to place bids, and administrators to manage auctions and deliveries. The system promotes transparency, enhances convenience, and eliminates the inefficiencies of traditional manual auctions.

---

## 📌 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [System Roles](#system-roles)
- [Technology Stack](#technology-stack)
- [Setup Instructions](#setup-instructions)
- [License](#license)

---

## 📖 About the Project

The **Online Auction System** streamlines auction processes through a responsive web interface. It provides:

- A secure and user-friendly experience for buyers, sellers, and admins.
- Instant bid updates and notifications.
- Transparent auction monitoring with robust backend logic.

---

## ✅ Features

- 🔐 User Authentication (Buyer, Seller, Admin)
- 📦 Product Listing & Management
- 🔨 Live Bidding with Expiry Timers
- 🛒 Wishlist Functionality
- 📈 Admin Dashboard for Order & Delivery Assignment
- 📨 Email-like Notifications (optional)
- 📱 Responsive Design

---

## 👥 System Roles

### 👤 Buyer
- Browse products
- Place bids
- Add to wishlist
- Track bidding history

### 🧑‍💼 Seller
- Upload and manage auction items
- Set asking price and expiry time
- Track auction status

### 🛠 Admin
- Manage users and roles
- Monitor all bids
- Assign delivery persons and finalize orders

---

## 🧰 Technology Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (default) or PostgreSQL
- **Tools:** Django Admin, Bootstrap (optional)

---

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/online-auction-system.git
   cd online-auction-system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Visit the app**
   Open your browser and go to `http://127.0.0.1:8000/`

---

## 📝 License

This project is for academic purposes only and follows all institutional plagiarism guidelines.

