# Conference Room Booking System

A Django-based web application for managing conference room reservations. Built for the **ISCG7420 Web Application Development** course.

---

## 1. Project Title and Description

**Conference Room Booking System**

This project is a full-featured web application that allows users to view available conference rooms, make reservations, and manage their bookings. Administrators have advanced controls to manage all rooms and reservations, including creating bookings on behalf of users. The system is designed with a focus on usability, security, and modern UX best practices.

---

## 2. Technologies Used

- **Python 3.x**
- **Django** (web framework)
- **SQLite** (default development database)
- **HTML5/CSS3** (custom templates and styling)

---

## 3. Features

- **View Available Rooms**: Browse all active conference rooms with details.
- **Make Reservations**: Book a room for a specific date and time slot.
- **Manage User's Own Reservations**: Users can view, edit, and cancel their own bookings.
- **Admin Management**:
  - Admins can view, edit, and delete all reservations and rooms.
  - Admins can create reservations on behalf of any user.
- **Email Notifications**: Reservation actions trigger email notifications (sent to the console for development).
- **UX Improvements**:
  - Calendar date picker for selecting reservation dates.
  - Time selection limited to 09:00–18:00 in 30-minute intervals.
  - Reserved time slots are disabled and visually distinct in the UI.

---

## 4. Admin and User Credentials (Demo Accounts)

> **Note:** Replace these with your own demo accounts as needed.

- **Admin Account**
  - Username: `admin`
  - Password: `adminpassword`
- **User Account**
  - Username: `user`
  - Password: `userpassword`

---

## 5. Installation and Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
7. **Access the app:**
   - Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 6. How to Test Features

- **Login** as a user or admin using the demo credentials above.
- **Browse rooms** and make a reservation using the calendar and time dropdowns.
- **Check your reservations** under "My Reservations".
- **Admin users** can access additional management features and create reservations for others.
- **Email notifications** will appear in the terminal/console (not sent to real email addresses).
- **Try booking overlapping times** to see validation in action.

---

## 7. AI Tools Disclosure

This project was developed with the assistance of AI tools, including **ChatGPT** and **Cursor**. These tools were used for code generation, documentation, and UX suggestions.

---

## 8. License and Disclaimer

This project is for educational purposes only as part of the ISCG7420 course. No warranty is provided. Please do not use in production without further security review and customization.

---
