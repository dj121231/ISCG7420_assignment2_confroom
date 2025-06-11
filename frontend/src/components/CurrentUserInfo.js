import React, { useEffect, useState } from "react";
import axiosInstance from "../axiosInstance";

const CurrentUserInfo = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await axiosInstance.get("/me/");
        setUser(response.data);
      } catch (error) {
        console.error("Error fetching user info:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchUser();
  }, []);

  if (loading) {
    return <div>Loading…</div>;
  }

  if (!user) {
    return <div>No user info available.</div>;
  }

  return (
    <div>
      <h1>Current User Info</h1>
      <p>Username: {user.username}</p>
      <p>Email: {user.email}</p>
      <p>Is Staff: {user.is_staff ? "Yes" : "No"}</p>
      <p>Is Superuser: {user.is_superuser ? "Yes" : "No"}</p>
    </div>
  );
};

export default CurrentUserInfo;
