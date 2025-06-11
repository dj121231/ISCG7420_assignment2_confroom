import React, { useState, useEffect } from "react";
import axiosInstance from "../axiosInstance";

const AdminReservations = () => {
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchReservations = async () => {
    try {
      const response = await axiosInstance.get("/reservations/");
      setReservations(response.data);
    } catch (err) {
      setError("Failed to load reservations");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReservations();
  }, []);

  const updateReservationStatus = (id, newStatus) => {
    setReservations((prevReservations) =>
      prevReservations.map((res) =>
        res.id === id ? { ...res, status: newStatus } : res
      )
    );
  };

  const handleApprove = async (id) => {
    try {
      await axiosInstance.post(`/reservations/${id}/approve/`);
      updateReservationStatus(id, "confirmed");
    } catch (err) {
      setError("Failed to approve reservation");
    }
  };

  const handleReject = async (id) => {
    try {
      await axiosInstance.post(`/reservations/${id}/reject/`);
      updateReservationStatus(id, "cancelled");
    } catch (err) {
      setError("Failed to reject reservation");
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: "red" }}>{error}</div>;
  if (reservations.length === 0) return <div>No reservations found</div>;

  return (
    <div>
      <h1>Admin Reservations</h1>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {reservations.map((res) => (
          <li
            key={res.id}
            style={{
              marginBottom: "20px",
              padding: "10px",
              border: "1px solid #ccc",
            }}
          >
            <div>
              <strong>Room:</strong> {res.room_name || res.room}
            </div>
            <div>
              <strong>User:</strong> {res.user_name || res.user}
            </div>
            <div>
              <strong>Date:</strong> {res.date}
            </div>
            <div>
              <strong>Time:</strong> {res.start_time} - {res.end_time}
            </div>
            <div>
              <strong>Status:</strong> {res.status}
            </div>
            {res.status === "pending" && (
              <div style={{ marginTop: "10px" }}>
                <button
                  onClick={() => handleApprove(res.id)}
                  style={{ marginRight: "10px", padding: "5px 10px" }}
                >
                  Approve
                </button>
                <button
                  onClick={() => handleReject(res.id)}
                  style={{ padding: "5px 10px" }}
                >
                  Reject
                </button>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AdminReservations;
