🧾 Online Auction System
An online auction platform built with Django that enables sellers to list products, buyers to place bids, and administrators to manage auctions and deliveries. The system promotes transparency, enhances convenience, and eliminates the inefficiencies of traditional manual auctions.
📖 About the Project
The Online Auction System streamlines auction processes through a responsive web interface. It provides:

A secure and user-friendly experience for buyers, sellers, and admins.

Instant bid updates and notifications.

Transparent auction monitoring with robust backend logic.

✅ Features
🔐 User Authentication (Buyer, Seller, Admin)

📦 Product Listing & Management

🔨 Live Bidding with Expiry Timers

🛒 Wishlist Functionality

📈 Admin Dashboard for Order & Delivery Assignment

📨 Email-like Notifications (optional)

📱 Responsive Design

👥 System Roles
👤 Buyer
Browse products

Place bids

Add to wishlist

Track bidding history

🧑‍💼 Seller
Upload and manage auction items

Set asking price and expiry time

Track auction status

🛠 Admin
Manage users and roles

Monitor all bids

Assign delivery persons and finalize orders

🧰 Technology Stack
Backend: Django (Python)

Frontend: HTML, CSS, JavaScript

Database: SQLite (default) or PostgreSQL

Tools: Django Admin, Bootstrap (optional)

⚙️ Setup Instructions
Clone the repository

bash
Copy
Edit
git clone https://github.com/yourusername/online-auction-system.git
cd online-auction-system
Create a virtual environment

bash
Copy
Edit
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run migrations

bash
Copy
Edit
python manage.py migrate
Create superuser

bash
Copy
Edit
python manage.py createsuperuser
Start the development server

bash
Copy
Edit
python manage.py runserver
Visit the app
Open your browser and go to http://127.0.0.1:8000/
