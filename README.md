# Astros Auction House

A full-featured online auction platform built with Django, designed for short-term bidding sessions featuring 3–4 products at a time. The platform includes real-time bidding, user authentication, winner selection, and administrative product management.

---

## Overview

Astros Auction House enables authenticated users to bid on live products during short, time-bound auction windows. After the auction ends, the system automatically selects a winner and sends them a confirmation email. Administrators can manage auctions through Django's built-in admin panel.

---

## Features

- User registration and login/logout  
- Real-time bidding with validation  
- Automatic winner selection after auction ends  
- Email notification to the winning bidder  
- Responsive design optimized for mobile and tablets  
- Admin interface for managing products and auctions  
- Support for up to five images per product  
- Full bid history display per product  
- Auction countdown timer integrated into the UI  

---

## Tech Stack

- Python  
- Django (Full-Stack Web Framework)  
- SQLite (Development Database)  
- Jinja2 (Templating Engine)  
- HTML/CSS (Frontend Markup & Styling)  
- Bootstrap (Responsive Design Framework)  
- JavaScript (Fetch API for asynchronous interaction)  
- pytz (Timezone Handling)  
- Django Admin Panel (for internal product and user management)  

---

## Getting Started

Follow the steps below to run the project locally:

1. Install Python (3.x) on your system.  
2. Clone the repository and navigate to the project folder.  
3. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/Scripts/activate  # On Windows use: venv\Scripts\activate
    ```

4. Install the dependencies

    ```bash
    pip install -r requirements.txt
    ```

5. Run the development server

    ```bash
    python manage.py runserver
    ```

5. Open the generated URL in your browser (typically http://127.0.0.1:8000/).

