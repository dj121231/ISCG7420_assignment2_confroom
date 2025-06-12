import React, { useEffect, useState } from "react";
import axiosInstance from "../axiosInstance";

const MyReservations = ({ isStaff, reservationChanged }) => {
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({
    title: "",
    date: "",
    start_time: "",
    end_time: "",
    description: "",
  });
  const [filterStatus, setFilterStatus] = useState("all");

  const fetchReservations = async () => {
    setLoading(true);
    try {
      const response = await axiosInstance.get("/my-reservations/");
      setReservations(response.data);
    } catch (err) {
      setError("Failed to load reservations.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReservations();
    // eslint-disable-next-line
  }, [reservationChanged]);

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to cancel this reservation?"))
      return;
    try {
      await axiosInstance.delete(`/reservations/${id}/`);
      fetchReservations();
    } catch (err) {
      setError("Failed to cancel reservation.");
    }
  };

  const handleEditClick = (res) => {
    setEditingId(res.id);
    setEditForm({
      title: res.title || "",
      date: res.date || "",
      start_time: res.start_time || "",
      end_time: res.end_time || "",
      description: res.description || "",
    });
  };

  const handleEditChange = (e) => {
    setEditForm({ ...editForm, [e.target.name]: e.target.value });
  };

  const handleEditCancel = () => {
    setEditingId(null);
    setEditForm({
      title: "",
      date: "",
      start_time: "",
      end_time: "",
      description: "",
    });
  };

  const handleEditSubmit = async (e, id) => {
    e.preventDefault();
    try {
      const response = await axiosInstance.put(
        `/reservations/${id}/`,
        editForm
      );
      setReservations(
        reservations.map((res) => (res.id === id ? response.data : res))
      );
      alert("Reservation updated successfully!");
      fetchReservations();
      setEditingId(null);
      setEditForm({
        title: "",
        date: "",
        start_time: "",
        end_time: "",
        description: "",
      });
    } catch (err) {
      setError("Failed to update reservation.");
    }
  };

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

  const filteredReservations = reservations.filter((res) =>
    filterStatus === "all" ? true : res.status === filterStatus
  );

  if (loading)
    return (
      <div style={{ fontSize: "0.95rem", color: "#666" }}>
        Loading reservations...
      </div>
    );
  if (error)
    return <div style={{ color: "#c62828", fontSize: "0.95rem" }}>{error}</div>;
  if (reservations.length === 0)
    return (
      <div style={{ fontSize: "0.95rem", color: "#666" }}>
        No reservations found.
      </div>
    );

  return (
    <div>
      <div className="card-title">My Reservations</div>
      <div className="tabs">
        <button
          className={`tab${filterStatus === "all" ? " active" : ""}`}
          onClick={() => setFilterStatus("all")}
        >
          <span className="tab-text">All</span>
        </button>
        <button
          className={`tab${filterStatus === "pending" ? " active" : ""}`}
          onClick={() => setFilterStatus("pending")}
        >
          <span className="tab-text">Pending</span>
        </button>
        <button
          className={`tab${filterStatus === "approved" ? " active" : ""}`}
          onClick={() => setFilterStatus("approved")}
        >
          <span className="tab-text">Approved</span>
        </button>
        <button
          className={`tab${filterStatus === "rejected" ? " active" : ""}`}
          onClick={() => setFilterStatus("rejected")}
        >
          <span className="tab-text">Rejected</span>
        </button>
      </div>
      {filteredReservations.length === 0 ? (
        <div
          style={{
            textAlign: "center",
            color: "#666",
            fontSize: "0.95rem",
            marginTop: "16px",
          }}
        >
          No reservations found.
        </div>
      ) : (
        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
          {filteredReservations.map((res) => (
            <li
              key={res.id}
              style={{
                position: "relative",
                marginBottom: "16px",
                padding: "12px",
                background: "#fff",
                borderRadius: "8px",
                border: "1px solid #e3e8ef",
                fontSize: "0.95rem",
              }}
            >
              <span className={`badge ${res.status}`}>
                {res.status.charAt(0).toUpperCase() + res.status.slice(1)}
              </span>
              <div style={{ marginBottom: "8px" }}>
                <strong style={{ color: "#1976d2" }}>
                  {res.title || "Untitled"}
                </strong>
              </div>
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
                  gap: "8px",
                  marginBottom: "12px",
                  color: "#555",
                }}
              >
                <div>
                  <strong style={{ color: "#666" }}>Date:</strong> {res.date}
                </div>
                <div>
                  <strong style={{ color: "#666" }}>Room:</strong>{" "}
                  {res.room_name || res.room}
                </div>
                <div>
                  <strong style={{ color: "#666" }}>Time:</strong>{" "}
                  {res.start_time.slice(0, 5)} - {res.end_time.slice(0, 5)}
                </div>
              </div>
              <div className="btn-group" style={{ marginTop: "8px" }}>
                {res.status === "pending" && (
                  <button
                    className="btn btn-primary"
                    onClick={() => handleEditClick(res)}
                    style={{ padding: "6px 12px", fontSize: "0.9rem" }}
                  >
                    Edit
                  </button>
                )}
                <button
                  className="btn btn-danger"
                  onClick={() => handleDelete(res.id)}
                  style={{ padding: "6px 12px", fontSize: "0.9rem" }}
                >
                  Cancel
                </button>
                {isStaff && res.status === "pending" && (
                  <>
                    <button
                      className="btn btn-primary"
                      style={{
                        background: "#388e3c",
                        padding: "6px 12px",
                        fontSize: "0.9rem",
                      }}
                      onClick={() => handleStatusChange(res.id, "approved")}
                    >
                      Approve
                    </button>
                    <button
                      className="btn btn-danger"
                      onClick={() => handleStatusChange(res.id, "rejected")}
                      style={{ padding: "6px 12px", fontSize: "0.9rem" }}
                    >
                      Reject
                    </button>
                  </>
                )}
              </div>
              {editingId === res.id && (
                <form
                  onSubmit={(e) => handleEditSubmit(e, res.id)}
                  style={{
                    marginTop: "12px",
                    padding: "12px",
                    background: "#f9fafd",
                    borderRadius: "6px",
                    fontSize: "0.95rem",
                  }}
                >
                  <div className="input-row">
                    <label className="label">Title</label>
                    <input
                      type="text"
                      name="title"
                      value={editForm.title}
                      onChange={handleEditChange}
                      className="input"
                      required
                      placeholder="Enter reservation title"
                    />
                  </div>
                  <div className="input-row">
                    <label className="label">Date</label>
                    <input
                      type="date"
                      name="date"
                      value={editForm.date}
                      onChange={handleEditChange}
                      className="input"
                      required
                    />
                  </div>
                  <div style={{ display: "flex", gap: "12px" }}>
                    <div className="input-row" style={{ flex: 1 }}>
                      <label className="label">Start Time</label>
                      <input
                        type="time"
                        name="start_time"
                        value={editForm.start_time}
                        onChange={handleEditChange}
                        className="input"
                        required
                      />
                    </div>
                    <div className="input-row" style={{ flex: 1 }}>
                      <label className="label">End Time</label>
                      <input
                        type="time"
                        name="end_time"
                        value={editForm.end_time}
                        onChange={handleEditChange}
                        className="input"
                        required
                      />
                    </div>
                  </div>
                  <div className="btn-group" style={{ marginTop: "8px" }}>
                    <button
                      type="submit"
                      className="btn btn-primary"
                      style={{ padding: "6px 12px", fontSize: "0.9rem" }}
                    >
                      Save Changes
                    </button>
                    <button
                      type="button"
                      className="btn btn-danger"
                      onClick={handleEditCancel}
                      style={{ padding: "6px 12px", fontSize: "0.9rem" }}
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MyReservations;
