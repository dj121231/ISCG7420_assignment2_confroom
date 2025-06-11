import React, { useEffect, useState } from "react";
import axiosInstance from "../axiosInstance";

const MyReservations = () => {
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

  useEffect(() => {
    fetchReservations();
  }, []);

  const handleDelete = async (id) => {
    try {
      await axiosInstance.delete(`/reservations/${id}/`);
      setReservations(reservations.filter((res) => res.id !== id));
    } catch (err) {
      setError("Failed to cancel reservation.");
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: "red" }}>{error}</div>;
  if (reservations.length === 0) return <div>No reservations found.</div>;

  return (
    <div>
      <h1>My Reservations</h1>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {reservations.map((res) => (
          <li
            key={res.id}
            style={{
              marginBottom: "20px",
              padding: "10px",
              border: "1px solid #ccc",
              borderRadius: "4px",
            }}
          >
            <div>
              <strong>Date:</strong> {res.date}
            </div>
            <div>
              <strong>Start:</strong> {res.start_time}
            </div>
            <div>
              <strong>End:</strong> {res.end_time}
            </div>
            <div>
              <strong>Room:</strong> {res.room_name || res.room}
            </div>
            <div>
              <strong>Status:</strong> {res.status}
            </div>
            <div style={{ marginTop: "10px" }}>
              <button
                onClick={() => alert("Edit form will be implemented soon")}
                style={{
                  marginRight: "10px",
                  padding: "5px 10px",
                  backgroundColor: "#4CAF50",
                  color: "white",
                  border: "none",
                  borderRadius: "4px",
                  cursor: "pointer",
                }}
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(res.id)}
                style={{
                  padding: "5px 10px",
                  backgroundColor: "#f44336",
                  color: "white",
                  border: "none",
                  borderRadius: "4px",
                  cursor: "pointer",
                }}
              >
                Cancel
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MyReservations;
