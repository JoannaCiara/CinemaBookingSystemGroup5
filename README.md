# CinemaBookingSystemGroup5
This project is a Django + Django REST Framework API for managing movies, halls, seats, screenings, and bookings with token-based authentication, automatic booking pricing, and validation rules to ensure reliable cinema operations.

**Group Members:**
- 150669 – Bryan Kipkorir
- 146740 – Joan Chuma
- 150875 – Mitchelle Kariuki
- 152506 – Esther Karuga
- 146414 – Wesley Ryan Mugele

## Setup Instructions
1. Install dependencies:
   bash
   pip install django djangorestframework djangorestframework-authtoken
   
2. Initialize project and app:
   bash
   django-admin startproject cinema_booking
   cd cinema_booking
   python manage.py startapp api
   
3. Add to `INSTALLED_APPS` in `settings.py`:
   python
   'rest_framework',
   'rest_framework.authtoken',
   'api',
   
4. Add REST framework global settings with `TokenAuthentication` and `IsAuthenticated` permissions.
5. Run migrations:
   bash
   python manage.py makemigrations
   python manage.py migrate
   
6. Create a superuser:
   bash
   python manage.py createsuperuser username GROUP9
   
7. Start the server:
   bash
   python manage.py runserver
   
8. Obtain an authentication token by posting to `/api-token-auth/`.

## Models and Relationships
- **Movie**: title, description, duration, rating, release date, language.
- **CinemaHall**: name, total seats, description.
- **Seat**: linked to hall, with row, number, seat type (Regular/VIP), unique per hall-row-number.
- **Screening**: links movie and hall with start time, base price, status; prevents overlaps; has `end_time` property.
- **Booking**: links screening and seat with customer details and price, calculated automatically from screening price, seat type, hall size, and discount codes.

**Relationships:**  
Movie → Screenings  
CinemaHall → Seats, Screenings  
Screening → Bookings  
Booking → Screening + Seat

## Views
DRF ModelViewSets provide CRUD for Movies, CinemaHalls, Seats, Screenings, and Bookings. They enforce authentication and can include custom actions like fetching available seats.

## Serializers
DRF ModelSerializers expose model fields. BookingSerializer ensures `price` and `booked_at` are read-only and validates against double-booking.

## URL Patterns
- `/api/movies/`
- `/api/halls/`
- `/api/seats/`
- `/api/screenings/`
- `/api/bookings/`
- `/api/bookings/?screening=<id>` (filter by screening)  
- `/admin/` (Django admin)  
- `/api-token-auth/` (obtain token)

## Testing
Django `TestCase` was used. Tests confirmed:
- Movies created and retrieved correctly.
- Seats uniqueness enforced.
- Screenings reject overlapping schedules.
- Bookings prevent duplicate seat allocation.
- Prices auto-calculated with seat type, hall size, and discount codes.
- API endpoints for Movies and Bookings require authentication.

**Results:** All tests passed successfully (`Ran 10 tests in 0.06s – OK`).


This project ensures reliable cinema operations (scheduling, seat allocation, bookings) with secure token-based authentication.
