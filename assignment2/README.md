# Conference Room Reservation System

A full-stack web application for reserving conference rooms, built with Django REST Framework (backend) and React.js (frontend).  
The system supports JWT-based authentication, user role distinction (admin and regular user), room and reservation management, an admin panel for approving/rejecting requests, and full CRUD operations with robust validation.

---

## 🛠️ Tech Stack

- **Backend:** Django, Django REST Framework, PostgreSQL
- **Frontend:** React.js (Create React App)
- **Authentication:** JWT (SimpleJWT)

---

## 📁 Folder Structure

```
ISCG7420_assignment2_1572184_dongjukim/
│
├── backend/           # Django project (manage.py, conference/, reservation/)
│   ├── conference/    # Django settings, urls, wsgi
│   └── reservation/   # App: models, views, serializers, urls, tests
│
├── frontend/          # React app (src/, public/, package.json)
│   └── src/           # React components, App.js, axiosInstance.js, etc.
│
└── .env               # Environment variables (see below)
```

---

## ⚡ Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd ISCG7420_assignment2_1572184_dongjukim
```

### 2. Backend Setup (Django)

- Create and activate a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Create a `.env` file in the root with:
  ```
  SECRET_KEY=your_secret_key
  DATABASE_URL=postgres://<user>:<password>@localhost:5432/confroom_db
  ```
- Run migrations and create superuser:
  ```bash
  python manage.py migrate
  python manage.py createsuperuser
  ```
- Start the backend server:
  ```bash
  python manage.py runserver
  ```
  The API will be available at [http://localhost:8000/api/](http://localhost:8000/api/)

### 3. Frontend Setup (React)

```bash
cd frontend
npm install
npm start
```

The frontend will run at [http://localhost:3000](http://localhost:3000)

- Optionally, create a `.env` in `frontend/`:
  ```
  REACT_APP_API_URL=http://localhost:8000/api
  ```

---

## ✨ Features

- User registration and login (JWT)
- User roles: Admin and Regular User
- View available conference rooms
- Create, edit, and cancel reservations
- Prevent overlapping/time-invalid reservations
- View your own reservations (filter by status)
- Admin panel: view all reservations, approve/reject requests
- Admin can manage all reservations
- Responsive, modern UI

---

## 🧪 Test Instructions

### Backend

- Run all tests:
  ```bash
  python manage.py test
  ```
- Generate coverage report (if `coverage` is installed):
  ```bash
  coverage run manage.py test
  coverage report
  coverage html  # for HTML report
  ```

---

## 🖼️ Screenshots

<!-- Add screenshots here -->

- Login Page
- Room List
- Reservation Form
- My Reservations
- Admin Panel

---

## ⚠️ Known Issues or Limitations

- [ ] Placeholder: List any known bugs or limitations here.

---

## 🔑 Admin Credentials (for testing)

- **Username:** `kimdongju`
- **Password:** `your_password_here`

---

## 🚀 Deployment Info

- Backend: [http://localhost:8000](http://localhost:8000)
- Frontend: [http://localhost:3000](http://localhost:3000)
- Runs locally by default.

---

## 🚀 Deployment on Render

Before deploying to Render, please confirm the following:

- **requirements.txt** (updated) – gunicorn is included (run: pip install gunicorn && pip freeze > requirements.txt).
- **render.yaml** – A new file (render.yaml) has been created in the project root with the following content (adjust envVars as needed):

```yaml
---
services:
  - type: web
    name: django-backend
    env: python
    buildCommand: ""
    startCommand: gunicorn conference.wsgi:application
    envVars:
      - key: SECRET_KEY
        value: your-secret-key
      - key: DATABASE_URL
        value: your-postgresql-connection-url
      - key: DEBUG
        value: "False"
---
```

- **manage.py** – Confirmed to exist at the project root.
- **runtime.txt** – A new file (runtime.txt) has been created at the project root with the content "python-3.10.13".

---

## 👤 Credits

**Author:** Dongju Kim (Unitec student)

---
