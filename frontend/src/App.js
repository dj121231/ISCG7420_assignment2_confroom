import React, { useEffect, useState } from "react";
import axiosInstance from "./axiosInstance";
import CurrentUserInfo from "./components/CurrentUserInfo";
import RoomList from "./components/RoomList";
import ReservationForm from "./components/ReservationForm";
import MyReservations from "./components/MyReservations";
import AdminPanel from "./components/AdminPanel";
import Login from "./components/Login";
import Signup from "./components/Signup";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

function App() {
  const [isStaff, setIsStaff] = useState(false);
  const [userLoading, setUserLoading] = useState(true);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (token) {
      try {
        const decoded = jwtDecode(token);
        setIsStaff(!!decoded.is_staff);
        setUser({
          username: decoded.username,
          email: decoded.email,
          is_staff: decoded.is_staff,
          is_superuser: decoded.is_superuser,
        });
      } catch (e) {
        setIsStaff(false);
        setUser(null);
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
      }
    } else {
      setIsStaff(false);
      setUser(null);
    }
    setUserLoading(false);
  }, []);

  if (userLoading) return <div>Loading user info...</div>;

  // Protected Route component
  const ProtectedRoute = ({ children }) => {
    if (!user) {
      return <Navigate to="/login" />;
    }
    return children;
  };

  return (
    <BrowserRouter>
      <header className="navbar">
        <div className="navbar-brand">Conference Room Reservation System</div>
        <nav className="navbar-links">
          {user ? (
            <>
              <a href="/" className="navbar-link">
                Home
              </a>
              {isStaff && (
                <a href="/admin-view" className="navbar-link">
                  Admin Panel
                </a>
              )}
              <button
                className="navbar-link"
                onClick={() => {
                  localStorage.removeItem("access");
                  localStorage.removeItem("refresh");
                  window.location.href = "/login";
                }}
                style={{
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                }}
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <a href="/login" className="navbar-link">
                Login
              </a>
              <a href="/signup" className="navbar-link">
                Sign Up
              </a>
            </>
          )}
        </nav>
      </header>

      {user && (
        <div className="userinfo-bar">
          <CurrentUserInfo user={user} />
        </div>
      )}

      <main className="main-container">
        <Routes>
          <Route
            path="/login"
            element={!user ? <Login /> : <Navigate to="/" />}
          />
          <Route
            path="/signup"
            element={!user ? <Signup /> : <Navigate to="/" />}
          />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <div className="dashboard">
                  <div className="main-content">
                    <div className="card-section small-card">
                      <ReservationForm />
                    </div>
                    <div className="card-section small-card">
                      <MyReservations isStaff={isStaff} />
                    </div>
                  </div>
                  <aside className="sidebar">
                    <div className="card-section small-card">
                      <RoomList />
                    </div>
                  </aside>
                </div>
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin-view"
            element={
              <ProtectedRoute>
                <div className="card-section small-card">
                  <AdminPanel isStaff={isStaff} />
                </div>
              </ProtectedRoute>
            }
          />
        </Routes>
        <footer className="footer">
          © 2025 Unitec - Web Application Assignment
        </footer>
      </main>
    </BrowserRouter>
  );
}

export default App;
