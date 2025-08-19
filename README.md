# 🎬 Cinema Booking API (GROUP9)

A Django + Django REST Framework (DRF) API for managing movies, halls, seats, screenings, and bookings.  
Includes authentication, pricing logic, booking validation, and **email confirmations with QR codes** for a real-world cinema experience.



## 👥 Group Members (Admins)
All members are registered as **admin users** in the system.

- 150669 – Bryan Kipkorir  
- 146740 – Joan Chuma  
- 150875 – Mitchelle Kariuki  
- 152506 – Esther Karuga  
- 146414 – Wesley Ryan Mugele  



## ⚙️ Technologies Used

- **Python 3**  
- **Django 5** – Backend framework  
- **Django REST Framework (DRF)** – REST API endpoints  
- **SQLite** – Development database  
- **SMTP (Gmail)** – For sending booking confirmation emails  
- **QR Code Generator (qrcode, Pillow)** – Attach QR codes to bookings  
- **HTML/CSS Templates** – Styled confirmation emails  
- **Token Authentication** – Secure API access  
- **Django Admin** – Management dashboard  
- **Unittest (Django TestCase)** – Automated testing  



## 🚀 Setup Instructions

1. Clone the repository:
   bash
   git clone https://github.com/JoannaCiara/CinemaBookingSystemGroup5.git
   cd CinemaBookingSystemGroup5
   

2. Install dependencies:
   bash
   pip install django djangorestframework djangorestframework-authtoken qrcode pillow
   

3. Run migrations:
   bash
   python manage.py makemigrations
   python manage.py migrate
   

4. Create a superuser (use your group ID as username, e.g. `GROUP9`):
   bash
   python manage.py createsuperuser --username GROUP9
   

5. Start the server:
   bash
   python manage.py runserver
   

6. Obtain an authentication token:
   http
   POST /api-token-auth/
   { "username": "GROUP9", "password": "yourpassword" }
   

---

## 📂 Models Overview

- **Movie** – Title, description, duration, rating, release date, language  
- **CinemaHall** – Name, total seats, description  
- **Seat** – Row, number, type (Regular/VIP), linked to a hall  
- **Screening** – Movie, hall, start time, base price, status (with overlap prevention)  
- **Booking** – Screening, seat, customer details, auto-calculated price, discounts, QR code  



## 🔑 Features

### 🎥 Movie & Screening Management
- CRUD operations for movies, halls, seats, screenings  
- Prevent overlapping screenings in the same hall  

### 💺 Smart Booking System
- Prevents double-booking of seats  
- Auto-calculates booking price:  
  * VIP surcharge  
  * Large hall surcharge  
  * Discount codes (`STUDENT10`, `VIP20`, `FREE`)  

### 🔐 Authentication & Security
- Token-based authentication  
- Global `IsAuthenticated` permissions for API access  

### 🎟 Email Booking Confirmations  
- Sends **booking confirmation email** after successful reservation  
- Includes customer details, movie, hall, seat, screening time, and price  
- Attaches a **QR code** for check-in  
- Supports **HTML + plain text** formats for professional styling  

📩 Example template:
```html
<h2>🎬 Booking Confirmation</h2>
<p>Hello {{ customer_name }},</p>
<p>Your booking is confirmed:</p>
<ul>
  <li><b>Movie:</b> {{ movie_title }}</li>
  <li><b>Hall:</b> {{ hall_name }}</li>
  <li><b>Seat:</b> {{ seat }}</li>
  <li><b>Time:</b> {{ start_time }}</li>
  <li><b>Price:</b> {{ price }}</li>
</ul>
{% if qr_code_url %}
<p><img src="{{ qr_code_url }}" alt="Your QR Code"></p>
{% endif %}
<p>Thank you for booking with us! 🍿</p>
```

---

## 🌐 API Endpoints

All endpoints are under `/api/`:

- `/movies/` – Manage movies  
- `/halls/` – Manage cinema halls  
- `/seats/` – Manage seats  
- `/screenings/` – Manage screenings  
- `/bookings/` – Manage bookings (filter by `?screening=<id>`)  

Authentication token:  
- `/api-token-auth/` – Obtain token  
- `/admin/` – Django admin dashboard  



## 🧪 Testing

Tests cover:  
- Movie creation/retrieval  
- Seat uniqueness  
- Screening overlap prevention  
- Booking seat double-checks  
- Price calculation (VIP, hall size, discount codes)  
- API authentication & endpoint responses  

✅ Example result:  

Ran 10 tests in 0.06s

OK



## 🎯 Summary

This project provides a **complete cinema booking API** with authentication, scheduling, pricing, QR-coded email confirmations, and admin features.  
It ensures **realistic cinema operations** while demonstrating strong use of **Django + DRF best practices**.


