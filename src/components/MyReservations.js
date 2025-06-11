import React, { useEffect, useState } from "react";
import axiosInstance from "../axiosInstance";

const MyReservations = () => {
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReservations = async () => {
      try {
        const response = await axiosInstance.get("/reservations/");
        setReservations(response.data);
      } catch (err) {
        setError("Failed to load reservations.");
      } finally {
        setLoading(false);
      }
    };
    fetchReservations();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: "red" }}>{error}</div>;
  if (reservations.length === 0) return <div>No reservations found.</div>;

  return (
    <div>
      <h1>My Reservations</h1>
      <ul>
        {reservations.map((res) => (
          <li key={res.id}>
            <strong>Date:</strong> {res.date} <br />
            <strong>Start:</strong> {res.start_time} <br />
            <strong>End:</strong> {res.end_time} <br />
            <strong>Room:</strong> {res.room} <br />
            <strong>Status:</strong> {res.status}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MyReservations;
