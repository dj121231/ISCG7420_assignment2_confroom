// AdminPanel.js - Admin interface for managing pending reservations
import React, { useEffect, useState } from "react";
import axiosInstance from "../axiosInstance";

const AdminPanel = ({ isStaff }) => {
  // State for reservations, loading, and error
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch pending reservations when component mounts or isStaff changes
  useEffect(() => {
    if (isStaff) {
      fetchReservations();
    }
    // eslint-disable-next-line
  }, [isStaff]);

  // Fetch all pending reservations
  const fetchReservations = async () => {
    setLoading(true);
    try {
      const response = await axiosInstance.get("/reservations/");
      setReservations(response.data.filter((res) => res.status === "pending"));
    } catch (err) {
      setError("Failed to load reservations.");
    } finally {
      setLoading(false);
    }
  };

  // Handle approve/reject actions (admin only)
  const handleStatusChange = async (id, newStatus) => {
    try {
      if (newStatus === "approved") {
        await axiosInstance.post(`/reservations/${id}/approve/`);
      } else if (newStatus === "rejected") {
        await axiosInstance.post(`/reservations/${id}/reject/`);
      }
      alert(
        `Reservation ${
          newStatus === "approved" ? "approved" : "rejected"
        } successfully!`
      );
      fetchReservations();
    } catch (err) {
      setError("Failed to update reservation status.");
    }
  };

  // Only admins can view this panel
  if (!isStaff) {
    return (
      <div style={{ color: "red", fontWeight: 600 }}>
        You are not authorized to view this page.
      </div>
    );
  }

  if (loading) return <div>Loading pending reservations...</div>;
  if (error) return <div style={{ color: "red" }}>{error}</div>;
  if (reservations.length === 0) return <div>No pending reservations.</div>;

  return (
    <div>
      <h2>Pending Reservations</h2>
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
            {/* Reservation details */}
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
            {/* Approve/Reject buttons */}
            <div style={{ marginTop: "10px" }}>
              <button
                onClick={() => handleStatusChange(res.id, "approved")}
                style={{
                  marginRight: "10px",
                  padding: "5px 10px",
                  backgroundColor: "#1976d2",
                  color: "white",
                  border: "none",
                  borderRadius: "4px",
                  cursor: "pointer",
                }}
              >
                Approve
              </button>
              <button
                onClick={() => handleStatusChange(res.id, "rejected")}
                style={{
                  padding: "5px 10px",
                  backgroundColor: "#b71c1c",
                  color: "white",
                  border: "none",
                  borderRadius: "4px",
                  cursor: "pointer",
                }}
              >
                Reject
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AdminPanel;
