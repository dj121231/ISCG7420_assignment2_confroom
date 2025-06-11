import React, { useEffect, useState } from "react";
import axiosInstance from "./axiosInstance";
import axios from "axios"; // Add axios import for the login request
import CurrentUserInfo from "./components/CurrentUserInfo";
import RoomList from "./components/RoomList";
import ReservationForm from "./components/ReservationForm";
import MyReservations from "./components/MyReservations";
import AdminReservations from "./components/AdminReservations";

// Automatic login - for development/testing only
axios
  .post("http://localhost:8000/api/token/", {
    username: "kimdongju",
    password: "kimdj2659123!",
  })
  .then((res) => {
    localStorage.setItem("access", res.data.access);
    localStorage.setItem("refresh", res.data.refresh);
    console.log("✅ JWT tokens saved successfully");
  })
  .catch((err) => {
    console.error("❌ Login failed", err);
  });

function App() {
  const [isAdmin, setIsAdmin] = useState(false);
  const [userLoading, setUserLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await axiosInstance.get("/me/");
        if (response.data.is_staff || response.data.is_superuser) {
          setIsAdmin(true);
        }
      } catch (err) {
        console.error("User fetch error", err);
      } finally {
        setUserLoading(false);
      }
    };
    fetchUser();
  }, []);

  if (userLoading) return <div>Loading user info...</div>;

  return (
    <div>
      <CurrentUserInfo />
      <RoomList />
      <ReservationForm />
      {isAdmin && <AdminReservations />}
      <MyReservations />
    </div>
  );
}

export default App;
