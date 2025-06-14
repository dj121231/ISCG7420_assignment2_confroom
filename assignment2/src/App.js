import React, { useEffect, useState } from "react";
import MyReservations from "./components/MyReservations";
import AdminReservations from "./components/AdminReservations";
import axiosInstance from "./axiosInstance";

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
        // Optionally handle error
      } finally {
        setUserLoading(false);
      }
    };
    fetchUser();
  }, []);

  if (userLoading) return <div>Loading user info...</div>;

  return (
    <>
      {isAdmin && <AdminReservations />}
      <MyReservations />
    </>
  );
}

export default App;
