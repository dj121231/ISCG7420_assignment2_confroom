// AdminReservations.js - Displays all reservations for admin management
import React, { useEffect, useState } from "react";
import axiosInstance from "../axiosInstance";

const AdminReservations = () => {
  // State for reservations, loading, and error
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch all reservations on mount
  useEffect(() => {
    fetchReservations();
  }, []);

  // Fetch all reservations (admin only)
  const fetchReservations = async () => {
    setLoading(true);
    try {
      const response = await axiosInstance.get("/reservations/");
      setReservations(response.data);
    } catch (err) {
      setError("Failed to load reservations.");
    } finally {
      setLoading(false);
    }
  };

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

  if (loading)
    return (
      <div style={{ fontSize: "0.95rem", color: "#666" }}>
        Loading reservations...
      </div>
    );
  if (error)
    return <div style={{ color: "#c62828", fontSize: "0.95rem" }}>{error}</div>;
  if (reservations.length === 0)
    return <div style={{ fontSize: "0.95rem" }}>No reservations found.</div>;

  // Render all reservations for admin
  return (
    <div>
      <div className="card-title">All Reservations (Admin)</div>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {reservations.map((res) => (
          <li
            key={res.id}
            style={{
              marginBottom: "16px",
              padding: "10px",
              border: "1px solid #ccc",
              borderRadius: "4px",
            }}
          >
            <div>
              <strong>Title:</strong> {res.title}
            </div>
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
              <strong>User:</strong> {res.user_name || res.user}
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
